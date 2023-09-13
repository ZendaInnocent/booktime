from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('products/<slug:tag>/', views.ProductListView.as_view(), name='product-list'),
    path(
        'product/<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'
    ),
    path('tag/<slug:tag>/', views.TagDetailView.as_view(), name='tag-detail'),
    path('add-to-basket/', views.add_to_basket, name='add-to-basket'),
    path('basket/', views.manage_basket, name='manage-basket'),
    path(
        'order/done/',
        TemplateView.as_view(template_name='main/order_done.html'),
        name='checkout-done',
    ),
    path(
        'order/address-list',
        views.AddressSelectionView.as_view(),
        name='address-select',
    ),
    path(
        'order-dashboard/',
        views.OrderView.as_view(),
        name='order-dashboard',
    ),
]
