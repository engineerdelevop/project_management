from django.conf.urls import url
# from django.contrib import admin
from django.urls import path
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from base import views
from .views import Inicio, Login, logoutUsuario

urlpatterns = [
    path('',login_required(Inicio.index), name="home"),
    path('accounts/login/',Login.as_view(), name='login'),
    path('logout/', login_required(logoutUsuario) , name ='logout')
]