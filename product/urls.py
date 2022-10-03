from django.shortcuts import render
from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
    path('', views.index, name="index"),
    path('detail/<slug:slug>/', views.detail, name="detail"),
    path('category/<int:category_id>/', views.category, name="category"),
    path('category-<int:category_id>/subcategory/<int:subcategory_id>/',
         views.subcategory,
         name="subcategory"),
    path('search/', views.search, name="search"),
    path('variation_on_change',
         views.variation_on_change,
         name="variation_on_change"),
    path('buy_product', views.buy_product, name="buy_product"),
]
