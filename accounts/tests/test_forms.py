from django.test import TestCase
from django import forms
from django.core import mail

from accounts.models import User
from accounts.forms import UserCreationForm


class AccountsFormsTest(TestCase):

    def test_valid_user_registration_form_sends_email(self):
        form = UserCreationForm({
            'email': 'testuser1@test.com',
            'name': 'Test User',
            'password1': 'hoonoruru',
            'password2': 'hoonoruru',
        })

        self.assertTrue(form.is_valid())

        with self.assertLogs('accounts', level='INFO') as cm:
            form.send_email()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(cm.output), 1)

    def test_invalid_user_registration_form(self):
        form = UserCreationForm({
            'email': 'testuser2@test.com',
            'name': 'Test User',
            'password1': 'hoonoruru',
        })

        self.assertFalse(form.is_valid())

    def test_arise_password_dont_match(self):
        form = UserCreationForm({
            'email': 'testuser@test.com',
            'name': 'Test User',
            'password1': 'hoonoruru',
            'password2': 'hoonodruru',
        })

        self.assertFalse(form.is_valid())
