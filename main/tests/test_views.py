from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from main import forms
from main.models import Product, Basket, BasketLine

User = get_user_model()


class TestMainAppViews(TestCase):

    def test_add_to_basket_loggedin_works(self):
        user1 = User.objects.create_user(
            name='sample name',
            email='sample@mail.com',
            password='adfsaidf',
        )

        cb = Product.objects.create(
            name="The cathedral and the bazaar",
            slug="cathedral-bazaar",
            price=Decimal("10.00"),
        )
        w = Product.objects.create(
            name="Microsoft Windows guide",
            slug="microsoft-windows-guide",
            price=Decimal("12.00"),
        )

        self.client.force_login(user1)
        response = self.client.get(
            reverse("main:add-to-basket"), {"product_id": cb.id})

        self.assertTrue(Basket.objects.filter(user=user1).exists())
        self.assertEqual(
            BasketLine.objects.filter(basket__user=user1).count(), 1)

        response = self.client.get(
            reverse("main:add-to-basket"), {"product_id": w.id})

        self.assertEqual(
            BasketLine.objects.filter(basket__user=user1).count(), 2)

    def test_home_page_works(self):
        response = self.client.get(reverse('main:home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')
        self.assertContains(response, 'BookTime')

    def test_about_page_works(self):
        response = self.client.get(reverse('main:about'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/about.html')

    def test_contact_page_works(self):
        response = self.client.get(reverse('main:contact'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/contact.html')
        self.assertIsInstance(response.context['form'], forms.ContactForm)

    def test_valid_form_in_contact_page_sends_mail(self):
        response = self.client.post(reverse('main:contact'), {
            'name': 'Test User',
            'message': 'Hi there!',
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_product_list_page_returns_active(self):
        Product.objects.create(
            name='the first product',
            slug='the-first-product',
            price=Decimal('2.00'),
            active=False,
        )
        Product.objects.create(
            name='the second product',
            slug='the-second-product',
            price=Decimal('21.00')
        )
        Product.objects.create(
            name='the third product',
            slug='the-third-product',
            price=Decimal('12.00'),
        )

        response = self.client.get(
            reverse('main:product-list', kwargs={'tag': "all"}))

        product_list = Product.objects.active().order_by('name')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['object_list']),
                         list(product_list))

    def test_product_list_page_filter_by_tags_and_active(self):
        cb = Product.objects.create(
            name="The cathedral and the bazaar",
            slug="cathedral-bazaar",
            price=Decimal("10.00"),
        )
        cb.tags.create(name="Open source", slug="opensource")
        Product.objects.create(
            name="Microsoft Windows guide",
            slug="microsoft-windows-guide",
            price=Decimal("12.00"),
        )

        response = self.client.get(
            reverse('main:product-list', kwargs={'tag': "opensource"}))

        self.assertEqual(response.status_code, 200)

        product_list = (Product.objects.active()
                        .filter(tags__slug='opensource')
                        .order_by('name'))
        self.assertEqual(list(response.context['object_list']),
                         list(product_list))
