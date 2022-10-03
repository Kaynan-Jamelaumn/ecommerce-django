from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('address/', views.address, name='address'),
    path('update-password/', views.user_update, name='update'),
    path('state-cities/', views.state_on_change, name='state_on_change'),
    path('address-register/', views.address_register, name='address-register'),
    path('address-delete/<int:id>/',
         views.address_delete,
         name='address_delete'),
]
