from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from main.models import Product, Basket, BasketLine
from accounts.models import Address
from main import factories

User = get_user_model()


class TestProductModel(TestCase):

    def test_product_string_representation(self):
        product = Product.objects.create(
            name='the first product',
            price=Decimal('2.00'),
        )

        self.assertEqual(str(product), product.name)

    def test_product_manager_works(self):
        factories.ProductFactory.create_batch(2, active=True)
        factories.ProductFactory(active=False)

        self.assertEqual(len(Product.objects.active()), 2)

    def test_create_order_works(self):
        p1 = factories.ProductFactory()
        p2 = factories.ProductFactory()

        user1 = factories.UserFactory()

        billing = factories.AddressFactory(user=user1)
        shipping = factories.AddressFactory(user=user1)

        basket = Basket.objects.create(user=user1)
        basketline = BasketLine.objects.create(product=p1, basket=basket)
        basketline = BasketLine.objects.create(product=p2, basket=basket)

        with self.assertLogs('main.models', level='INFO') as cm:
            order = basket.create_order(billing, shipping)

        self.assertGreaterEqual(len(cm.output), 2)

        order.refresh_from_db()

        self.assertEqual(order.user, user1)
        self.assertEqual(order.billing_address1, billing.address1)
        self.assertEqual(order.shipping_address1, shipping.address1)
        self.assertEqual(order.orderlines.count(), 2)

        orderlines = order.orderlines.all()

        self.assertEqual(orderlines[0].product, p1)
        self.assertEqual(orderlines[1].product, p2)
