from django.urls import resolve, reverse

from main import views


def test_home_url_resolves():
    home_url = reverse('main:home')
    assert resolve(home_url).func == views.home_view


def test_about_url_resolves():
    about_url = reverse('main:about')
    assert resolve(about_url).func == views.about_view


def test_contact_url_resolves():
    contact_url = reverse('main:contact')
    assert resolve(contact_url).func.view_class == views.ContactView
