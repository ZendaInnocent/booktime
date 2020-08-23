import logging

from django.test import TestCase
from django.urls import reverse

from accounts.forms import UserCreationForm
from accounts.models import User, Address

logger = logging.getLogger(__name__)


class AccountsAppViewsTest(TestCase):

    def test_user_registration_view_works(self):
        response = self.client.get(reverse('accounts:signup'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')
        self.assertIsInstance(response.context['form'], UserCreationForm)

    def test_user_registration_view_submission_works(self):
        data = {
            'email': 'someone@domain.com',
            'name': 'Someone There',
            'password1': 'ofsdoadsfoisadfh9',
            'password2': 'ofsdoadsfoisadfh9'
        }

        response = self.client.post(
            reverse('accounts:signup'), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        self.assertTrue(User.objects.filter(
            email='someone@domain.com').exists())

    def test_address_string_representation(self):
        user = User.objects.create_user(
            email='test@user1.com',
            name='test user1',
            password='fdosigfsd',
        )
        address = Address(
            user=user,
            name='Someone Moro',
            address1='Majengo - Sumbawanga',
            address2='',
            zip_code='187',
            city='Sumbawanga',
            country='TZ',
        )

        self.assertEqual(
            str(address),
            'Someone Moro, Majengo - Sumbawanga, , 187, Sumbawanga, TZ')

    def test_address_create_stores_a_user(self):
        user1 = User.objects.create_user(
            email='test@user1.com',
            name='test user1',
            password='fdosigfsd',
        )
        post_data = {
            'name': 'some name',
            'address1': 'some line',
            'address2': '',
            'zip_code': '187',
            'city': 'swaxasd',
            'country': 'TZ'
        }

        self.client.force_login(user1)
        response = self.client.post(reverse('accounts:address-add'),
                                    post_data)

        self.assertTrue(response.status_code, 200)
        self.assertTrue(
            Address.objects.filter(user=user1).exists()
        )

    def test_address_list_page_returns_only_owned(self):
        user1 = User.objects.create_user(
            email='test@user1.com',
            name='test user1',
            password='fdosigfsd',
        )
        user2 = User.objects.create_user(
            email='test@user2.com',
            name='test user2',
            password='fsjdoidsfk',
        )

        address1 = Address(
            user=user1,
            name='some name',
            address1='some line',
            address2='another line',
            city='swax',
        )
        address2 = Address(
            user=user2,
            name='some name',
            address1='some line',
            address2='another line',
            city='swaxasd',
        )

        self.client.force_login(user1)
        response = self.client.get(reverse('accounts:address-list'))

        self.assertEqual(response.status_code, 200)

        address_list = Address.objects.filter(user=user1)

        self.assertEqual(
            list(response.context['object_list']), list(address_list)
        )
