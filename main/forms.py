import logging

from django import forms
from django.forms import inlineformset_factory
from django.core.mail import send_mail

from main.models import Basket, BasketLine

logger = logging.getLogger(__name__)


BasketLineFormSet = inlineformset_factory(
    Basket,
    BasketLine,
    fields=('quantity', ),
    extra=0,
)


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your Name',
            })
        )
    message = forms.CharField(widget=forms.Textarea(
        attrs={
            'placeholder': "Your Message",
            'rows': '4',
        }
    ))

    def send_mail(self):
        logger.info('Sending email to Customer Service unit')

        message = f"From: {self.cleaned_data['name']}\n\nMessage:\n\
            {self.cleaned_data['message']}"

        send_mail(
            'Mail from the site',
            message,
            'contact@domain.com',
            ['customerservices@domain.com'],
            fail_silently=False,
        )
