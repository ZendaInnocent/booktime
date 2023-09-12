from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpResponse
from django.urls import reverse
from pytest_django.asserts import assertContains, assertTemplateUsed

from main import forms
from main.models import Basket, BasketLine, Product

User: type[AbstractBaseUser] = get_user_model()


def test_add_to_basket_loggedin_works(client) -> None:
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

    client.force_login(user1)
    client.get(reverse("main:add-to-basket"), {"product_id": cb.id})

    assert Basket.objects.filter(user=user1).exists()
    assert BasketLine.objects.filter(basket__user=user1).count() == 1

    client.get(reverse("main:add-to-basket"), {"product_id": w.id})

    assert BasketLine.objects.filter(basket__user=user1).count() == 2


def test_home_page_works(client) -> None:
    response: HttpResponse = client.get(reverse('main:home'))

    assert response.status_code == 200
    assertTemplateUsed(response, 'main/home.html')
    assertContains(response, 'BookTime')


def test_about_page_works(client) -> None:
    response: HttpResponse = client.get(reverse('main:about'))

    assert response.status_code == 200
    assertTemplateUsed(response, 'main/about.html')


def test_contact_page_works(client) -> None:
    response: HttpResponse = client.get(reverse('main:contact'))

    assert response.status_code == 200
    assertTemplateUsed(response, 'main/contact.html')
    assert isinstance(response.context['form'], forms.ContactForm)


def test_valid_form_in_contact_page_sends_mail(client) -> None:
    response: HttpResponse = client.post(
        reverse('main:contact'),
        {
            'name': 'Test User',
            'message': 'Hi there!, how are you doing?',
        },
    )
    assert response.status_code, 302
    # assertRedirects(response, '/')


def test_product_list_page_returns_active(client) -> None:
    Product.objects.create(
        name='the first product',
        slug='the-first-product',
        price=Decimal('2.00'),
        active=False,
    )
    Product.objects.create(
        name='the second product', slug='the-second-product', price=Decimal('21.00')
    )
    Product.objects.create(
        name='the third product',
        slug='the-third-product',
        price=Decimal('12.00'),
    )

    response: HttpResponse = client.get(
        reverse('main:product-list', kwargs={'tag': "all"})
    )

    product_list = Product.objects.active().order_by('name')

    assert response.status_code == 200
    assert list(response.context['object_list']) == list(product_list)


def test_product_list_page_filter_by_tags_and_active(client) -> None:
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

    response: HttpResponse = client.get(
        reverse('main:product-list', kwargs={'tag': "opensource"})
    )

    assert response.status_code == 200

    product_list = (
        Product.objects.active().filter(tags__slug='opensource').order_by('name')
    )
    assert list(response.context['object_list']) == list(product_list)
