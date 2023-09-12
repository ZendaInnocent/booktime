import logging

from django import forms
from django.core.mail import send_mail
from django.forms import inlineformset_factory

from accounts.models import Address
from main.models import Basket, BasketLine

from .widgets import PlusMinusNumberInput

logger = logging.getLogger(__name__)


BasketLineFormSet = inlineformset_factory(
    Basket,
    BasketLine,
    fields=('quantity',),
    extra=0,
    widgets={'quantity': PlusMinusNumberInput()},
)


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Your Name',
            }
        ),
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': "Your Message (Not less than 4 words)",
                'rows': '4',
            }
        )
    )

    def clean_message(self):
        message = self.cleaned_data.get('message', '')
        num_words = len(message.split())
        if num_words < 4:
            raise forms.ValidationError("Not enough words!")
        return message

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


class AddressSelectionForm(forms.Form):
    billing_address = forms.ModelChoiceField(queryset=None)
    shipping_address = forms.ModelChoiceField(queryset=None)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = Address.objects.filter(user=user)
        self.fields['billing_address'].queryset = queryset
        self.fields['shipping_address'].queryset = queryset
