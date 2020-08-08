from django.test import TestCase

from accounts.models import User


class AccountsModelsTests(TestCase):

    def test_can_save_users(self):
        user1 = User.objects.create_user(
            email='test1@user.com',
            name='test user 1',
            password='helootheree',
        )
        user2 = User.objects.create_user(
            email='test2@user.com',
            name='test user 2',
            password='helootheree',
        )

        users = User.objects.all()

        self.assertEqual(len(users), 2)

    def test_raise_message_when_create_user_with_invalid_email(self):
        self.assertRaisesMessage(ValueError,
                                 'Users must have an email address',
                                 User.objects.create_user, email='',
                                 name='odsif')

    def test_user_string_representation(self):
        user = User(email='some@web.com', name='Someone',
                    password='odufsohdof')
        user.save()

        self.assertEqual(str(user), user.email)

    def test_staff_property_for_non_superuser(self):
        user = User.objects.create_user(
                    email='test@user.com',
                    name='test user',
                )

        self.assertFalse(user.is_staff)

    def test_staff_property(self):
        superuser = User.objects.create_superuser(
                    email='superuser@admin.com',
                    name='super user'
                )
        self.assertTrue(superuser.is_staff)

    # def test_address_string_representation(self):
    #     address = Address(
    #         user = self.user,
    #         zip_code = '187',
    #         city = 'Sumbawanga',
    #     )

    #     self.assertEqual(str(address), self.user.full_name)
