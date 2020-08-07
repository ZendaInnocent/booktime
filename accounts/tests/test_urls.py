from django.test import TestCase
from django.urls import reverse, resolve

from accounts import views


class TestAccountsAppUrls(TestCase):

    def test_register_url_resolves(self):
        register_url = reverse('accounts:signup')
        self.assertEqual(resolve(register_url).func.view_class, views.UserRegistrationView)
