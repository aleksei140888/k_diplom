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
    path('product/<int:product_id>/', views.product, name='product'),
    path('card/product/add/', views.card_add_item, name='card_add_item'),
    path('card/<int:card_id>/', views.card, name='shop_card'),
    path('payment/make/', views.payment_make, name='payment_make'),
    path('shop/make/', views.make_shop, name='make_shop'),
    path('<int:shop_id>/', views.shop, name='shop'),
    path('', views.all_shops, name='all_shops'),
]
