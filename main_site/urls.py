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
from django.urls import path, include

from main_site import views

urlpatterns = [
    path('user_profile/<int:user_id>/', views.user_page, name='user_page'),
    path('user/<int:user_id>/', views.user, name='user'),
    path('load_profile/', views.load_profile, name='load_profile'),
    path('auth/', views.auth_page, name='auth_page'),
    path('auth/sign', views.auth_sign, name='auth_sign'),
    path('auth/register', views.auth_register, name='auth_register'),
    path('auth/signout', views.auth_signout, name='auth_signout'),
    path('', views.home_page, name='home_page'),

]
