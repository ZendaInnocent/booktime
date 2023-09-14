import logging
from decimal import Decimal

import pytest
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.files.images import ImageFile
from django.urls import reverse

from main.models import Basket, BasketLine, Product, ProductImage


def test_thumbnails_are_generated_on_save(caplog) -> None:
    product = Product.objects.create(
        name='The cathedral and the bazaar', price=Decimal('10.00')
    )

    with open('main/fixtures/capital.png', 'rb') as f:
        image = ProductImage(
            product=product,
            image=ImageFile(f, name='tctb.png'),
        )

        with caplog.at_level(logging.INFO, logger='main.signals'):
            image.save()

    assert len(caplog.records) >= 1

    # check if the generated thumbnail is what expected
    image.refresh_from_db()

    with open('main/fixtures/capital-thumb.png', 'rb') as f:
        expected_content: bytes = f.read()
        assert image.thumbnail.read() == expected_content

    # delete generated files
    image.thumbnail.delete(save=False)
    image.image.delete(save=False)


@pytest.mark.xfail()
def test_basket_merge_when_login_works(client) -> None:
    user1: AbstractBaseUser = get_user_model().objects.create(
        email='ome22@test.com',
    )
    cb: Product = Product.objects.create(
        name="The cathedral and the bazaar",
        slug="cathedral-bazaar",
        price=Decimal("10.00"),
    )
    w: Product = Product.objects.create(
        name="Microsoft Windows guide",
        slug="microsoft-windows-guide",
        price=Decimal("12.00"),
    )
    basket: Basket = Basket.objects.create(user=user1)
    BasketLine.objects.create(basket=basket, product=cb, quantity=2)
    client.get(
        reverse('main:add-to-basket'),
        {'product_id': w.id},
    )

    assert auth.get_user(client).is_authenticated

    basket = Basket.objects.get(user=user1)

    assert basket.count == 3
