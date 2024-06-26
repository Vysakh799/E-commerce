from django.urls import path
from . import views

urlpatterns = [
    #index
    path('',views.index),

    #products
    path('products/<pk>',views.products),
    path('products1/<pk>/<pk1>',views.products1),

    #login and logout
    path('login',views.login),
    path('logout',views.logout),
    path('signup',views.signup),

    #catograry
    path('catagory/<type>',views.catagory),

    #userdetails
    path('user',views.user),
    path('yourorders',views.yourorders),
    path('address',views.address),
    path('add_address',views.add_address),
    path('update_address/<pk>',views.update_address),
    path('remove_address/<pk>',views.remove_address),
    path('update_user',views.update_user),
    path('update',views.update),
    path('update_password',views.update_password),

    #contact section
    path('contact',views.contact),

    #cart
    path('add_cart/<pk>',views.cart),
    path('cart/',views.view_cart),
    path('delete_item/<pk>',views.delete_item),
    path('incri_count/<pk>',views.incri_count),
    path('decri_count/<pk>',views.decri_count),
    path('order_address/<pk1>',views.order_address),
    path('order_address1/<pk>',views.order_address1),

    #order
    path('add_address_order/<data2>',views.add_address_order),
]
