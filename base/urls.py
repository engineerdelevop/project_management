from django.conf.urls import url
# from django.contrib import admin
from django.urls import path
from django.contrib.auth import login,logout
from base import views
from .views import Inicio, Login

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('', Inicio.as_view(), name='home')
    path('home/',views.Inicio.index, name="home"),
    path('',Login.as_view(), name='login'),
]