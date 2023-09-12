import logging

from django.core import mail

from main import forms


def test_valid_contact_form_sends_mail(caplog) -> None:
    form = forms.ContactForm(
        {'name': 'Test User', 'message': 'Hi there!, how are you doing?'}
    )

    assert form.is_valid()

    with caplog.at_level(logging.INFO, logger='main.forms'):
        form.send_mail()

    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == 'Mail from the site'

    assert len(caplog.records) >= 1


def test_invalid_contact_form() -> None:
    form = forms.ContactForm(
        {
            'name': 'TEst User',
        }
    )

    assert not form.is_valid()
