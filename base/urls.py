from django.conf.urls import url
# from django.contrib import admin
from django.urls import path
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from base import views
from .views import Inicio, Login, logoutUsuario, DetalleProyecto, listaProyecto, ListarActividad, ViewProyectosForms, actualziarProyecto, viewCrearActividad, actualizarActividad, actualizarActividadTrabajador

urlpatterns = [
    ### Login y logout
    path('',login_required(Inicio.index), name='home'),
    path('accounts/login/',Login.as_view(), name='login'),
    path('logout/', login_required(logoutUsuario) , name ='logout'),

    ### Lista de proyectos
    path('lista_proyectos/',listaProyecto.as_view(), name = 'lista_proyecto'),

    ### Listar actividad
    path('lista_actividades/',ListarActividad.as_view(), name = 'lista_actividad'),

    ### Listar actividad usuario
    path('lista_actividades_usuario/',ListarActividad.as_view(), name = 'lista_actividad_usuario'),

    ### Forms crear proyecto
    path('crear_Proyecto/',ViewProyectosForms.CreacionProyecto, name = 'crear_proyecto'),
    path('guardar_Proyecto/',ViewProyectosForms.ProcesarFormsProyecto, name = 'guardar_proyecto'),

    ### detalle proyecto
    path('<slug:slug>/',DetalleProyecto.as_view(), name = 'detalle_proyecto'),

    ### actualizar proyecto
    path('actualziar_Proyecto/<slug>/',actualziarProyecto.modificarProyecto, name = 'actualizar_proyecto'),

    ### crear Actividad
    path('crear_actividad/<slug>/',viewCrearActividad.crearActividad, name = 'crear_actividad'),
    path('guardar_actividad/<slug>/',viewCrearActividad.crearActividadCargue, name = 'guardar_actividad'),
    
    ### actualizar actividad
    path('actualizar_actividad/<id>/',actualizarActividad.modificarActividad, name = 'actualizar_actividad'),

    ### actualizar actividad trabajador
    path('actualizar_actividad_trabajador/<id>/',actualizarActividadTrabajador.modificarActividadtrabajador, name = 'actualizar_actividad_trabajador'),

    ### No autorizado
    path('no_autorizado/',Inicio.index, name = 'no_autorizado'),
    
]