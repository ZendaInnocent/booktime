from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.views import generic

from . import forms
from main.models import Product, ProductTag


class HomeView(generic.TemplateView):
    template_name = 'main/home.html'


class AboutView(generic.TemplateView):
    template_name = 'main/about.html'


class ContactView(generic.FormView):
    form_class = forms.ContactForm
    template_name = 'main/contact.html'
    success_url = '/'

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)


class ProductListView(generic.ListView):
    template_name = 'main/product_list.html'
    paginate_by = 2

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
    paginate_by = 2

    def get_queryset(self):
        tag = self.kwargs['tag']
        products = Product.objects.active().filter(tags__slug=tag)
        return products.order_by('name')
