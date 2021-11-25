from django.contrib.auth.models import Permission
from django.db.models.aggregates import Count
from django.shortcuts import render, redirect
from django.http import HttpResponse

# For login
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout

# importar formularios
from .forms import FormularioLogin, FormsProyecto, FormsProyectoActualizar, FormsCrearActividades, FormsActualizarActividades, FormsActualizarActividadesTrabajador

# importar los mensajes
from django.contrib import messages

# para listar proyectos
from django.views.generic import ListView, View, DetailView

# Para permisos
from django.contrib.auth.mixins import LoginRequiredMixin

# modelos
from .models import *

# resumen principal, sumar, restar, contar

import pandas as pd
from django_pandas.io import read_frame # conda install -c conda-forge django-pandas
from django.db.models import Sum, Max, Min, Avg, Count, OuterRef, Subquery

# Paginator
from django.core.paginator import Paginator

# date
from datetime import date

# importar decorators

from .decarators import allowed_users



# Create your views here.

#####################
###### Login y logout

# Se crea clase para el inicio de sesión
class Login(FormView):
    template_name = 'login.html'
    form_class = FormularioLogin
    success_url = reverse_lazy('base:home')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)

    def dispatch(self,request,*args,**kwargs):

        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self,form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)

# se crea función para el logout, automaticamente se redirige al login
def logoutUsuario(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')


#####################
###### actualiación numero de tareas

def ActualizarActividades(id):
    try:
        proyecto = Proyecto.objects.get(id = id)
    except:
        proyecto = None
    actividades = Actividad.objects.filter(proyecto_id = proyecto).count()
    updateActividades = Proyecto.objects.get(id = id)
    updateActividades.numero_activdades = actividades
    updateActividades.save()

#####################
###### calcular hoy

def hoy():
    return date.today()


#####################
###### home resumen proyectos

class Inicio(LoginRequiredMixin, ListView):

    def index(request):

        if request.user.groups.filter(name__in=['Gerente', 'Supervisor']).exists():

            ########### Cuenta el numero de proyectos
            NoProyectos = Proyecto.objects.values('nombre').count() 
            ########### Cuenta el numero de proyectos sin iniciar
            NoSinIniciar = Proyecto.objects.filter(estado_id = 1).count()
            ########### Cuenta el numero de proyectos en proceso
            NoEnProceso = Proyecto.objects.filter(estado_id = 2).count()
            ########### Cuenta e numero de proyectos finalizados
            NoFinalizados = Proyecto.objects.filter(estado_id = 3).count()

            ########### Graficas pie estado proyectos
            qs = Proyecto.objects.select_related('cliente').annotate(cliente_count=Count('cliente'))
            lenQs = len(qs)
            empresas = []
            for q in qs:
                empresas.append(q.cliente.nombreCliente)
            
            df_empresa = pd.DataFrame()
            df_empresa['Empresas'] = empresas
            df_empresa['Cantidad'] = 1

            GruopyBtEmpresa = df_empresa.groupby(['Empresas']).sum().reset_index()
            labels = GruopyBtEmpresa['Empresas'].tolist()
            data = GruopyBtEmpresa['Cantidad'].tolist()


            ########### Grafica presupuestos
            labelsPresupuesto = []
            dataPresupuestos = []
            dataEjecutado= []

            queryset = Proyecto.objects.order_by('id')
            for proyecto in queryset:
                labelsPresupuesto.append(proyecto.nombre)
                dataPresupuestos.append(proyecto.presupuesto)
                dataEjecutado.append(proyecto.presupuesto_ejecutado)

            ########### muestra los proyectos
            proyectos = Proyecto.objects.get_queryset().order_by('estado_id')

            ########### Actualiza las actividades de cada proyecto de manera automatica en el inicio del home
            obj= Proyecto.objects.values('id').values_list('id', flat=True)
            list1=list(obj)
            for i in list1:
                lista_actualización = ActualizarActividades(i)
                i

            ########### paginator que muestra 2 proyectos por pagina
            paginator = Paginator(proyectos,2)
            pagina = request.GET.get('page')
            proyectos = paginator.get_page(pagina)


            ##########  Usuario activo

            #NombreUsuario = User.objects.get(pk = 1)
        
        
            context = {
                ######## resumen proyectos
                'NoProyectos':NoProyectos,
                'NoSinIniciar':NoSinIniciar,
                'NoEnProceso':NoEnProceso,
                'NoFinalizados':NoFinalizados,

                ######## proyectos para paginator
                'proyectos':proyectos,

                ######## para graficas
                #### presupuesto 
                'labelsPresupuesto':labelsPresupuesto,
                'dataPresupuestos':dataPresupuestos,
                'dataEjecutado':dataEjecutado,

                #### distribución clientes
                'data':data,
                'labels':labels,
                
                ####
                'lista_actualización':lista_actualización,

                #### hoy
                'hoy':hoy()
            }
            
            return render(request,'home.html',context)
        
        else:


            #Listar las actiidades del usuario 
            userid = request.user.id
            listarActividades = Actividad.objects.filter(responsable_id = userid).order_by('estado_id')

            ########### Cuenta el numero de actividades 
            NodActividades = Actividad.objects.filter(responsable_id = userid).count()
            ########### Cuenta el numero de actividades sin proceso
            NoSinIniciar = Actividad.objects.filter(responsable_id = userid).filter(estado_id = 1).count()
            ########### Cuenta el numero de actividades en proceso
            NoEnProceso = Actividad.objects.filter(responsable_id = userid).filter(estado_id = 2).count()
            ########### Cuenta e numero de actividades finalizados
            NoFinalizados = Actividad.objects.filter(responsable_id = userid).filter(estado_id = 3).count()

            
            ########### paginator que muestra 2 proyectos por pagina
            paginator = Paginator(listarActividades,2)
            pagina = request.GET.get('page')
            listarActividades = paginator.get_page(pagina)
            
            contexto = {
                'listarActividades':listarActividades,
                'NodActividades':NodActividades,
                'NoSinIniciar':NoSinIniciar,
                'NoEnProceso':NoEnProceso,
                'NoFinalizados':NoFinalizados,
            }
            return render(request,'listaActividadesUsuario.html',contexto)


#####################
###### información proyectos
class DetalleProyecto(LoginRequiredMixin, DetailView):
    
    def get(self,request,slug,*args,**kwargs):
        
        # Mostrar información del proyecto
        NombreProyecto = Proyecto.objects.get(slug = slug)

        # listar actividades del proyecto
        ListarActividades = Actividad.objects.filter(proyecto_id = NombreProyecto).order_by('estado_id')

        # alerta actividad
        def alerta_proyecto():
            if NombreProyecto.estado_id == 1 and NombreProyecto.fecha_final <= hoy():
                return 'Proyecto retrasado'
            elif NombreProyecto.estado_id == 2 and NombreProyecto.fecha_final <= hoy():
                return 'Proyecto retrasado'
            elif NombreProyecto.estado_id == 3 and NombreProyecto.fecha_final <= hoy():
                return 'Proyecto finalizado'
            elif NombreProyecto.estado_id == 1 and NombreProyecto.fecha_inicial >= hoy():
                return 'Proyecto sin iniciar'
            elif NombreProyecto.estado_id == 1 and NombreProyecto.fecha_final >= hoy():
                return 'Proyecto sin iniciar'
            elif NombreProyecto.estado_id == 2 and NombreProyecto.fecha_final >= hoy():
                return 'Proyecto en proceso'
            elif NombreProyecto.estado_id == 2 and NombreProyecto.fecha_final >= hoy():
                return 'Proyecto finalizado'
            else:
                return 'Sin iniciar'

        #pie avance actividad
        frame = read_frame(ListarActividades)

        if request.user.groups.filter(name__in=['Gerente', 'Supervisor']).exists():
            contexto = {
                'NombreProyecto':NombreProyecto,
                'ListarActividades':ListarActividades,
                'alerta_proyecto':alerta_proyecto()
            }
            print(alerta_proyecto())
            return render(request,'proyecto.html',contexto)
        else:
            return render(request,'noAutorizado.html')

class listaProyecto(LoginRequiredMixin, DetailView):

    def get(self,request,*args,**kwargs):

        # listar proyectos
        ListarProyectos = Proyecto.objects.get_queryset().order_by('estado_id')

        ########### paginator que muestra 4 proyectos por pagina
        paginator = Paginator(ListarProyectos,4)
        pagina = request.GET.get('page')
        ListarProyectos = paginator.get_page(pagina)
        
        #if request.user.groups.Gerente or request.user.groups.Supervisor:
        if request.user.groups.filter(name__in=['Gerente', 'Supervisor']).exists():
            contexto = {
                'ListarProyectos':ListarProyectos,
            }
            return render(request,'listaProyectos.html',contexto)
        else:
            return render(request,'noAutorizado.html')


class ListarActividad(LoginRequiredMixin, DetailView):

    def get(self,request,*args,**kwargs):

        listarActividades = Actividad.objects.get_queryset().order_by('estado_id')


        ########### paginator que muestra 4 proyectos por pagina
        paginator = Paginator(listarActividades,4)
        pagina = request.GET.get('page')
        listarActividades = paginator.get_page(pagina)
        if request.user.groups.filter(name__in=['Gerente', 'Supervisor']).exists():
            contexto = {
                'listarActividades':listarActividades,
            }
            return render(request,'listaActividades.html',contexto)
        else:
            return render(request,'noAutorizado.html')


#################
## Formularios

#####################
###### Creación view formulario proyecto

class ViewProyectosForms(LoginRequiredMixin, HttpResponse, ListView):

    @allowed_users(allowed_roles = ['Gerente','Supervisor'])
    def CreacionProyecto(request):

        form = FormsProyecto()

        contexto = {
            'form':form, # forms proyecto
        }
        return render(request,'crearProyecto.html',contexto)

    @allowed_users(allowed_roles = ['Gerente','Supervisor'])
    def ProcesarFormsProyecto(request):

        form = FormsProyecto(request.POST)

        if form.is_valid():
            form.save()
            form = FormsProyecto()

        contexto = {
            'form':form, # forms proyecto
            'mensaje': 'OK'
        }
        return render(request,'crearProyecto.html',contexto)
        
#####################
###### Actualizar proyecto

class actualziarProyecto(HttpResponse, ListView):

    @allowed_users(allowed_roles = ['Gerente','Supervisor'])
    def modificarProyecto(request, slug, ):

    
        NombreProyecto = Proyecto.objects.get(slug = slug)

        form = FormsProyectoActualizar(instance=NombreProyecto)

        contexto = {
            'form':form,
            'mensaje': 'OK'
        }

        if request.method == 'POST':
            form = FormsProyectoActualizar(request.POST, instance=NombreProyecto)
            if form.is_valid():
                form.save()
                messages.success(request, 'Proyecto actualizado correctamente.')
            else:
                messages.error(request, 'Proyecto no actualizado, verifique la información.')
                messages.error(request, form.errors)
            contexto['form'] = form
  
        return render(request,'actualizarProyecto.html',contexto)

#####################
###### Crear actividad

class viewCrearActividad(LoginRequiredMixin, HttpResponse):

    @allowed_users(allowed_roles = ['Gerente','Supervisor'])
    def crearActividad(request,slug):

        NombreProyecto = Proyecto.objects.get(slug = slug)
        
        form = FormsCrearActividades()

        contexto = {
            'form':form, # forms actividad
            'NombreProyecto':NombreProyecto,
        }

        return render(request,'crearActividad.html',contexto)

    @allowed_users(allowed_roles = ['Gerente','Supervisor'])
    def crearActividadCargue(request,slug):

        NombreProyecto = Proyecto.objects.get(slug = slug)

        #form = FormsCrearActividades(request.POST, instance=NombreProyecto)
        form = FormsCrearActividades(request.POST)
        contexto = {
            'form':form, # forms proyecto
            'mensaje': 'OK',
            'NombreProyecto':NombreProyecto,
        }

        if request.method == 'POST':
            #form = FormsCrearActividades(request.POST)
            if form.is_valid():
                form.save()
                #NombreProyecto.proyecto = request.proyecto
                form = FormsCrearActividades()
                messages.success(request, 'Actividad creada correctamente.')
            else:
                messages.error(request, 'Actividad no creada, verifique la información.')
                messages.error(request, form.errors)

            contexto['form'] = form

        return render(request,'crearActividad.html',contexto)

#####################
###### actualización actividades

class actualizarActividad(LoginRequiredMixin, HttpResponse):

    def modificarActividad(request,id):

        #NombreProyecto = Proyecto.objects.get(slug = slug)

        ListarActividades = Actividad.objects.get(id = id)

        form = FormsActualizarActividades(instance=ListarActividades)

        if request.user.groups.filter(name__in=['Gerente', 'Supervisor']).exists():
            contexto = {
                'form':form,
                'mensaje': 'OK'
            }

            if request.method == 'POST':
                form = FormsActualizarActividades(request.POST, instance=ListarActividades)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Actividad actualizada correctamente.')
                else:
                    messages.error(request, 'Actividad no actualizada, verifique la información.')
                    messages.error(request, form.errors)
                contexto['form'] = form
    
            return render(request,'actualizarActividad.html',contexto)
        else:
            return render(request,'noAutorizado.html')


class actualizarActividadTrabajador(LoginRequiredMixin, HttpResponse):

    def modificarActividadtrabajador(request,id):

        #NombreProyecto = Proyecto.objects.get(slug = slug)

        ListarActividades = Actividad.objects.get(id = id)

        form = FormsActualizarActividadesTrabajador(instance=ListarActividades)

        contexto = {
            'form':form,
            'mensaje': 'OK'
        }

        if request.method == 'POST':
            form = FormsActualizarActividadesTrabajador(request.POST, instance=ListarActividades)
            if form.is_valid():
                form.save()
                messages.success(request, 'Actividad actualizada correctamente.')
            else:
                messages.error(request, 'Actividad no actualizada, verifique la información.')
                messages.error(request, form.errors)
            contexto['form'] = form
  
        return render(request,'actualizarActividadTrabajador.html',contexto)
