from django.urls import path
# from django.views.generic import DetailView

from . import views
from main.models import Product

app_name = 'main'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('products/<slug:tag>/', views.ProductListView.as_view(),
         name='product-list'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(),
         name='product-detail'),
    path('tag/<slug:tag>/', views.TagDetailView.as_view(),
         name='tag-detail'),
]
