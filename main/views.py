from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django import forms as django_forms
from django.db import models as django_models

import django_filters
from django_filters.views import FilterView

from . import forms
from main.models import Product, ProductTag, Basket, BasketLine, Order


class AddressSelectionView(generic.FormView):
    form_class = forms.AddressSelectionForm
    template_name = 'main/address_list.html'
    success_url = reverse_lazy('main:checkout-done')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        del self.request.session['basket_id']
        basket = self.request.basket
        basket.user = self.request.user
        basket.create_order(
            form.cleaned_data['billing_address'],
            form.cleaned_data['shipping_address']
        )
        return super().form_valid(form)


def manage_basket(request):
    if not request.basket or request.basket.is_empty():
        return render(request, 'main/basket.html', {'formset': None})
    else:
        formset = forms.BasketLineFormSet(instance=request.basket)

    if request.method == 'POST':
        formset = forms.BasketLineFormSet(
            request.POST, instance=request.basket)
        if formset.is_valid():
            formset.save()

        return redirect(reverse('main:manage-basket'))

    return render(request, 'main/basket.html', {'formset': formset})


def add_to_basket(request):
    product = get_object_or_404(Product, pk=request.GET.get('product_id'))
    basket = request.basket

    if not request.basket:
        user = request.user if request.user.is_authenticated else None
        basket = Basket.objects.create(user=user)
        request.session['basket_id'] = basket.id

    basketline, created = BasketLine.objects.get_or_create(
        basket=basket, product=product)

    if not created:
        basketline.quantity += 1
        basketline.save()

    return HttpResponseRedirect(
        reverse('main:product-detail', args=(product.slug, )))


class HomeView(generic.TemplateView):
    template_name = 'main/home.html'


class AboutView(generic.TemplateView):
    template_name = 'main/about.html'


class ContactView(SuccessMessageMixin, generic.FormView):
    form_class = forms.ContactForm
    template_name = 'main/contact.html'
    success_url = '/'
    success_message = ('Your message has sent successful. '
                       'We will get to you shortly.')

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)


class ProductListView(generic.ListView):
    template_name = 'main/product_list.html'
    paginate_by = 6

    def get_queryset(self):
        tag = self.kwargs['tag']
        self.tag = None

        if tag != 'all':
            self.tag = get_object_or_404(ProductTag, slug=tag)

        if self.tag:
            products = Product.objects.active().filter(tags=self.tag)
        else:
            products = Product.objects.active()

        return products.order_by('name')


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'main/product_detail.html'


class TagDetailView(generic.ListView):
    template_name = 'main/tag_detail.html'
    paginate_by = 6

    def get_queryset(self):
        tag = self.kwargs['tag']
        products = Product.objects.active().filter(tags__slug=tag)
        return products.order_by('name')


class DateInput(django_forms.DateInput):
    input_type = 'date'


class OrderFilter(django_filters.FilterSet):

    class Meta:
        model = Order

        fields = {
            'user__email': ['icontains'],
            'status': ['exact'],
            'date_updated': ['gt', 'lt'],
            'date_added': ['gt', 'lt'],
        }

        filter_overrides = {
            django_models.DateTimeField: {
                'filter_class': django_filters.DateFilter,
                'extra': lambda f: {
                    'widget': DateInput}}}


class OrderView(LoginRequiredMixin, UserPassesTestMixin, FilterView):
    filterset_class = OrderFilter

    def test_func(self):
        return self.request.user.is_staff
