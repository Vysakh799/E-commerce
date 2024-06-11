from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('products/<pk>',views.products),
    path('login',views.login),
    path('logout',views.logout),
    path('signup',views.signup),
    path('catagory/<type>',views.catagory),
    path('user',views.user),
    path('yourorders',views.yourorders),
    path('address',views.address),
    path('add_address',views.add_address)
]
