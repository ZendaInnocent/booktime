from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from main.models import Product, Basket, BasketLine
from accounts.models import Address

User = get_user_model()


class TestProductModel(TestCase):

    def test_product_string_representation(self):
        product = Product.objects.create(
            name='the first product',
            price=Decimal('2.00'),
        )

        self.assertEqual(str(product), product.name)

    def test_product_manager_works(self):
        Product.objects.create(
            name='the first product',
            price=Decimal('2.00'),
            active=False,
        )
        Product.objects.create(
            name='the second product',
            price=Decimal('21.00')
        )
        Product.objects.create(
            name='the third product',
            price=Decimal('12.00'),
        )

        self.assertEqual(len(Product.objects.active()), 2)

    def test_create_order_works(self):
        p1 = Product.objects.create(
            name="The cathedral and the bazaar",
            price=Decimal("10.00"),)
        p2 = Product.objects.create(
            name="Pride and Prejudice", price=Decimal("2.00"))

        user1 = User.objects.create_user(
            name="user1", email='user1@sample.co', password="pw432joij")

        billing = Address.objects.create(
            user=user1,
            name="John Kimball",
            address1="127 Strudel road",
            city="Morogoro",
            country="tz",
        )
        shipping = Address.objects.create(
            user=user1,
            name="John Kimball",
            address1="123 Deacon road",
            city="Morogoro",
            country="tz",
        )

        basket = Basket.objects.create(user=user1)
        basketline = BasketLine.objects.create(product=p1, basket=basket)
        basketline = BasketLine.objects.create(product=p2, basket=basket)

        with self.assertLogs('main.models', level='INFO') as cm:
            order = basket.create_order(billing, shipping)

        self.assertGreaterEqual(len(cm.output), 1)

        order.refresh_from_db()

        self.assertEqual(order.user, user1)
        self.assertEqual(order.billing_address1, '127 Strudel road')
        self.assertEqual(order.shipping_address1, '123 Deacon road')
        self.assertEqual(order.orderlines.count(), 2)

        orderlines = order.orderlines.all()

        self.assertEqual(orderlines[0].product, p1)
        self.assertEqual(orderlines[1].product, p2)
