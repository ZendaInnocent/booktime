from django.shortcuts import render
from django.views.generic import (
    CreateView, ListView, UpdateView, DeleteView)
from django.urls import reverse_lazy

from accounts import forms
# from accounts.models import Address


class UserRegistrationView(CreateView):
    form_class = forms.UserCreationForm
    template_name = 'registration/signup.html'
    success_url = '/'


# class AddressListView(ListView):
#     model = Address
#     template_name = 'accounts/address_list.html'

#     def get_queryset(self):
#         return self.model.objects.filter(user=self.request.user)


# class AddressCreateView(CreateView):
#     model = Address
#     template_name = 'accounts/address_create.html'
#     fields = ('zip_code', 'city', 'country', )
#     success_url = reverse_lazy('accounts:address-list')

#     def form_valid(self, form):
#         if form.is_valid():
#             form.instance.user = self.request.user
#         return super().form_valid(form)


# class AddressUpdateView(UpdateView):
#     model = Address
#     fields = ('zip_code', 'city', 'country', )
#     template_name = 'accounts/address_update.html'
#     success_url = reverse_lazy('accounts:address-list')


# class AddressDeleteView(DeleteView):
#     model = Address
#     success_url = reverse_lazy('accounts:address-list')
