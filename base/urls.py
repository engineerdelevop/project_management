from django.conf.urls import url
# from django.contrib import admin
from django.urls import path
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from base import views
from .views import Inicio, Login, logoutUsuario, DetalleProyecto, listaProyecto, ViewProyectosForms

urlpatterns = [
    path('',login_required(Inicio.index), name='home'),
    path('accounts/login/',Login.as_view(), name='login'),
    path('logout/', login_required(logoutUsuario) , name ='logout'),
    path('lista_proyectos/',listaProyecto.as_view(), name = 'lista_proyecto'),
    ### Forma crear proyecto
    path('crear_Proyecto/',ViewProyectosForms.CreacionProyecto, name = 'crear_proyecto'),
    path('guardar_Proyecto/',ViewProyectosForms.ProcesarFormsProyecto, name = 'guardar_proyecto'),
    ### detalle proyecto
    path('<slug:slug>/',DetalleProyecto.as_view(), name = 'detalle_proyecto'),
    
    
    
    
]