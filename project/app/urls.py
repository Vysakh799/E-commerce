from django.urls import path
from . import views

urlpatterns = [
    #index
    path('',views.index),

    #products
    path('products/<pk>',views.products),
    path('products1/<pk>/<pk1>',views.products1),
    path('see_all',views.see_all),

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
    path('forgot_password',views.forgot_password),
    path('forgot_password_mail',views.forgot_password_mail),

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
    path('add_order/<data2>',views.add_order,name='add_order'),
    path('add_order_address/<int:data2>',views.add_order_address),
    path('track_order/<pk>',views.track_order),
    path('ordered_products',views.ordered_products),
    path('replace_product',views.replace_product),
    path('update_order_address/<pk>/<int:data2>',views.update_order_address),
    path('remove_order_address/<pk>/<int:data2>',views.remove_order_address),
    path('delete_order/<pk>',views.delete_order),
    path('order_history',views.order_history),
    path("replace_reorder/<pk>",views.replace_reorder),
    path("buyagain",views.buyagain),

    #buynow
    path('buynow/<pk>',views.buynow),

    #Search
    path('search_func',views.search_func),



    #payment
    path('payment/<int:data2>',views.payment),
    path('razorpay/callback/',views.callback),



    #Admin
    path('admin_login',views.admin_login),
    path('admin_logout',views.admin_logout),
    path('admin_addproduct',views.add_product),
    path('edit/<pk>',views.edit),
    path('delete/<pk>',views.delete),

]
