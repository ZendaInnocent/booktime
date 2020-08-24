from django.contrib.auth import get_user_model

import factory
from factory import fuzzy

from .models import Product
from accounts.models import Address

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    email = 'user@site.com'

    class Meta:
        model = User
        django_get_or_create = ('email', )


class ProductFactory(factory.django.DjangoModelFactory):
    price = fuzzy.FuzzyDecimal(1.0, 1000.0, 2)

    class Meta:
        model = Product


class AddressFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Address
