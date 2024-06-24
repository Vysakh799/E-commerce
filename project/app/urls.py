from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('cart/<pk>',views.cart),
    path('products/<pk>',views.products),
    path('products1/<pk>/<pk1>',views.products1),
    path('login',views.login),
    path('logout',views.logout),
    path('signup',views.signup),
    path('catagory/<type>',views.catagory),
    path('user',views.user),
    path('yourorders',views.yourorders),
    path('address',views.address),
    path('add_address',views.add_address),
    path('update_address/<pk>',views.update_address),
    path('remove_address/<pk>',views.remove_address),
    path('update_user',views.update_user),
    path('update',views.update),
    path('update_password',views.update_password),
    path('contact',views.contact),
]
