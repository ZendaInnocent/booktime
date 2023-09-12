import logging
from decimal import Decimal

from django.contrib.auth import get_user_model

from main import factories
from main.models import Basket, BasketLine, Product

User = get_user_model()


def test_product_string_representation() -> None:
    product = Product.objects.create(
        name='the first product',
        price=Decimal('2.00'),
    )

    assert str(product) == product.name

    def test_product_manager_works() -> None:
        factories.ProductFactory.create_batch(2, active=True)
        factories.ProductFactory(active=False)

        assert len(Product.objects.active()) == 2


def test_create_order_works(caplog) -> None:
    p1 = factories.ProductFactory()
    p2 = factories.ProductFactory()

    user1 = factories.UserFactory()

    billing = factories.AddressFactory(user=user1)
    shipping = factories.AddressFactory(user=user1)

    basket = Basket.objects.create(user=user1)
    BasketLine.objects.create(product=p1, basket=basket)
    BasketLine.objects.create(product=p2, basket=basket)

    with caplog.at_level(logging.INFO, logger='main.models'):
        order = basket.create_order(billing, shipping)

    assert len(caplog.records) == 2

    order.refresh_from_db()

    assert order.user == user1
    assert order.billing_address1 == billing.address1
    assert order.shipping_address1 == shipping.address1
    assert order.orderlines.count() == 2

    orderlines = order.orderlines.all()

    assert orderlines[0].product == p1
    assert orderlines[1].product == p2
