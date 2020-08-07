import pytest
import selenium

from django.test import TestCase
from django.urls import reverse, resolve

from main import views


class TestMainAppUrls(TestCase):

    def test_home_url_resolves(self):
        home_url = reverse('main:home')
        self.assertEqual(resolve(home_url).func.view_class, views.HomeView)

    def test_about_url_resolves(self):
        about_url = reverse('main:about')
        self.assertEqual(resolve(about_url).func.view_class, views.AboutView)

    def test_contact_url_resolves(self):
        contact_url = reverse('main:contact')
        self.assertEqual(resolve(contact_url).func.view_class,
                         views.ContactView)
