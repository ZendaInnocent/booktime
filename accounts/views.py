import logging

from django.shortcuts import render
from django.views.generic import (
    CreateView, ListView, UpdateView, DeleteView)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts import forms
from accounts.models import Address

logger = logging.getLogger(__name__)


class UserRegistrationView(CreateView):
    form_class = forms.UserCreationForm
    template_name = 'registration/signup.html'
    success_url = '/'

    def form_valid(self, form):
        if form.is_valid():
            email = form.cleaned_data['email']
            logger.info(
                "New signup for email=%s through SignupView", email
            )
            form.send_email()
        return super().form_valid(form)


class AddressListView(LoginRequiredMixin, ListView):
    model = Address
    template_name = 'accounts/address_list.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class AddressCreateView(LoginRequiredMixin, CreateView):
    model = Address
    template_name = 'accounts/address_create.html'
    fields = ('name', 'address1', 'address2', 'zip_code', 'city', 'country', )
    success_url = reverse_lazy('accounts:address-list')

    def form_valid(self, form):
        if form.is_valid():
            form.instance.user = self.request.user
        return super().form_valid(form)


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = Address
    fields = ('name', 'address1', 'address2', 'zip_code', 'city', 'country', )
    template_name = 'accounts/address_update.html'
    success_url = reverse_lazy('accounts:address-list')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class AddressDeleteView(LoginRequiredMixin, DeleteView):
    model = Address
    success_url = reverse_lazy('accounts:address-list')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
