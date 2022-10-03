from django.urls import include, path
from . import views

app_name = 'cart'
urlpatterns = [
    path('', views.cart_view, name='view'),
    path('add/', views.cart_add, name='add'),
    path('remove/<int:id>', views.remove_item_from_session, name='remove'),
]
