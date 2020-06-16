"""live_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from creative_shop import views

urlpatterns = [
    path('success_payment/', views.success_payment, name='success_payment'),
    path('error_payment/', views.error_payment, name='error_payment'),
    path('shop_get_pursaches/', views.shop_get_pursaches, name='shop_get_pursaches'),
    path('shop_get_owner_cards/', views.shop_get_owner_cards, name='shop_get_owner_cards'),
    path('shop_get_owner_products/', views.shop_get_owner_products, name='shop_get_owner_products'),
    path('shop_set_in_delivery_status/<int:card_item_id>/', views.shop_set_in_delivery_status, name='shop_set_in_delivery_status'),
    path('shop_set_in_completed_status/<int:card_item_id>/', views.shop_set_in_completed_status, name='shop_set_in_completed_status'),
    path('product/<int:product_id>/', views.product, name='product'),
    path('card/product/delete/', views.card_item, name='card_delete_item'),
    path('card/product/add/', views.card_item, name='card_add_item'),
    path('card/<int:card_id>/', views.card, name='shop_card'),
    path('payment/make/', views.payment_make, name='payment_make'),
    path('shop/delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('shop/add_product/', views.add_product, name='add_product'),
    path('shop/edit_product/', views.edit_product, name='edit_product'),
    path('shop/edit_product_window/<int:product_id>/', views.edit_product_window, name='edit_product_window'),
    path('shop/make/', views.make_shop, name='make_shop'),
    path('<int:shop_id>/', views.shop, name='shop'),
    path('', views.all_shops, name='all_shops'),
]
