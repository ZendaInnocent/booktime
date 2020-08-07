from decimal import Decimal

from django.test import TestCase

from main.models import Product


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
