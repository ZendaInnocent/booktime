from django.test import TestCase
from django.core import mail

from main import forms


class TestMainAppForms(TestCase):

    def test_valid_contact_form_sends_mail(self):
        form = forms.ContactForm({
            'name': 'Test User',
            'message': 'Hi there!'
        })

        self.assertTrue(form.is_valid())

        with self.assertLogs('main.forms', level='INFO') as cm:
            form.send_mail()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Mail from the site')

        self.assertGreaterEqual(len(cm.output), 1)

    def test_invalid_contact_form(self):
        form = forms.ContactForm({
            'name': 'TEst User',
        })

        self.assertFalse(form.is_valid())
