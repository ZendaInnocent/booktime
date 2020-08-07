from django.test import TestCase
from django.urls import reverse

from accounts.forms import UserCreationForm
from accounts.models import CustomUser, Address


class AccountsAppViewsTest(TestCase):

    def test_user_registration_view(self):
        response = self.client.get(reverse('accounts:signup'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')
        self.assertIsInstance(response.context['form'], UserCreationForm)

    def test_address_list_page_returns_only_owned(self):
        user1 = CustomUser.objects.create_user(
            email='test@user1.com',
            name='test user1',
            password='fdosigfsd',
        )
        user2 = CustomUser.objects.create_user(
            email='test@user2.com',
            name='test user2',
            password='fsjdoidsfk',
        )

        address1 = Address(
            user=user1,
            city='swax',
        )
        address2 = Address(
            user=user2,
            city='swaxasd',
        )

        self.client.login(email='test@user1.com', password='fdosigfsd')
        # response = self.client.get(reverse('accounts:address-list'))

        # self.assertEqual(response.status_code, 200)

        address_list = Address.objects.filter(user=user1)

        # self.assertEqual(
        #     list(response.context['object_list']), list(address_list)
        # )

    def test_address_create_stores_a_user(self):
        user1 = CustomUser.objects.create_user(
            email='test@user1.com',
            name='test user1',
            password='fdosigfsd',
        )
        post_data = {
            'zip_code': '187',
            'city': 'swaxasd',
            'country': 'TZ',
        }

        self.client.login(email='test@user1.com', password='fdosigfsd')
        response = self.client.post(reverse('accounts:address-create'),
                                    post_data)

        self.assertTrue(response.status_code, 200)
        self.assertTrue(
            Address.objects.filter(user=user1).exists()
        )
