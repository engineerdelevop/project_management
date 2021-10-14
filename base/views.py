from django.db.models.aggregates import Count
from django.shortcuts import render
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
from .forms import FormularioLogin, FormsProyecto

# para listar proyectos
from django.views.generic import ListView, View, DetailView

# 
from .models import *

# resumen principal, sumar, restar, contar

import pandas as pd
from django_pandas.io import read_frame # conda install -c conda-forge django-pandas
from django.db.models import Sum, Max, Min, Avg, Count, OuterRef, Subquery

# Paginator
from django.core.paginator import Paginator

# pivot table
from django_pivot.pivot import pivot
from django_pivot.histogram import histogram




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
###### home resumen proyectos

class Inicio(ListView):

    def index(request):

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
            # 
            'lista_actualización':lista_actualización,
        }
        return render(request,'home.html',context)

#####################
###### información proyectos
class DetalleProyecto(DetailView):
    
    def get(self,request,slug,*args,**kwargs):
        
        # Mostrar información del proyecto
        try:
            NombreProyecto = Proyecto.objects.get(slug = slug)
            
        except:
            NombreProyecto = None

        # Numerar las actividades del proyecto 
        #actividades = Actividad.objects.filter(proyecto_id = NombreProyecto).count()
        
        #updateActividades = Proyecto.objects.get(slug = slug)
        #updateActividades.numero_activdades = actividades
        #updateActividades.save()

        # listar actividades del proyecto
        ListarActividades = Actividad.objects.filter(proyecto_id = NombreProyecto).order_by('estado_id')
        # data = []
    
        # for ListarActividad in ListarActividades:
        #     data.append(ListarActividad.meta)

        #pie avance actividad
        frame = read_frame(ListarActividades)

        
        contexto = {
            'NombreProyecto':NombreProyecto,
            'ListarActividades':ListarActividades,
        }
        return render(request,'proyecto.html',contexto)


class listaProyecto(DetailView):

    def get(self,request,*args,**kwargs):

        # listar proyectos
        ListarProyectos = Proyecto.objects.get_queryset().order_by('estado_id')

        ########### paginator que muestra 4 proyectos por pagina
        paginator = Paginator(ListarProyectos,4)
        pagina = request.GET.get('page')
        ListarProyectos = paginator.get_page(pagina)

        contexto = {
            'ListarProyectos':ListarProyectos,
        }
        return render(request,'listaProyectos.html',contexto)

#################
## Formularios


#####################
###### Creación view formulario proyecto

class ViewProyectosForms(HttpResponse):


    def CreacionProyecto(request):

        form = FormsProyecto()

        contexto = {
            'form':form, # forms proyecto
        }
        return render(request,'crearProyecto.html',contexto)

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
        
