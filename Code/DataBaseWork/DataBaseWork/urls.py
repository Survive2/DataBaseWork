"""DataBaseWork URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from app01 import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.login, name="home"),
    path('login/', views.login),
    path('index/', views.index),
    path('add/', views.add),
    path('goods_find/', views.goods_find),
    path('goods_find_result/', views.goods_find),
    path('update/', views.update),
    path('delete/', views.delete),
    path('cs_find/', views.cs_find),
    path('cs_find_result/', views.cs_find),
    path('lh_find/', views.lh_find),
    path('lh_find_result/', views.lh_find),
    path('order_find/', views.order_find),
]
