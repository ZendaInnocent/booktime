from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

from . import forms
from main.models import Product, ProductTag, Basket, BasketLine


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
