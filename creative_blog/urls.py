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

from creative_blog import views

urlpatterns = [
    path('blog_get_masterclasses/', views.blog_get_masterclasses, name='blog_get_masterclasses'),
    path('delete_master_class/<int:article_id>/', views.delete_master_class, name='delete_master_class'),
    path('edit_master_class_window/<int:article_id>/', views.edit_master_class_window, name='edit_master_class_window'),
    path('article/create/', views.article_create, name='article_create'),
    path('article/delete/<int:article_id>/', views.article_delete, name='article_delete'),
    path('article/<int:article_id>/', views.article, name='article'),
    path('<int:user_id>/', views.blog, name='blog'),
    path('', views.all_blogs, name='all_blogs'),
]
