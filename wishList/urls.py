"""wishList URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from .views import home, logout_usr, createAcc, login, additem, editAccount, add_item, refresh_list,refresh_hlist

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('createAccount/', createAcc, name="createAcc"),
    path('logout/', logout_usr, name="logout_usr"),
    path('login/', login, name="login"),
    path('additem/', additem, name="additem"),
    path('editAccount/', editAccount, name="editAccount"),
    path('api/', include('myapi.urls')),
    path('add_item/', add_item, name="add_item"),
    path('list/', refresh_list, name="refresh_list"),
    path('hlist/', refresh_hlist, name="refresh_hlist")
]
