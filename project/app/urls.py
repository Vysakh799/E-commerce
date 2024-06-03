from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('products/<pk>',views.products),
    path('login',views.login),
    path('signup',views.signup),
]
