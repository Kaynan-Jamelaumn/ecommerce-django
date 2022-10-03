from django.urls import path
from . import views

app_name = 'order'
urlpatterns = [
    path('<int:id>', views.order_info, name='order_info'),
    path('pay/', views.pay, name='pay'),

]
