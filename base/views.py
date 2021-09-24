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
from .forms import FormularioLogin

# 
from django.views.generic import ListView

# 
from .models import *

# resumen principal, sumar, restar, contar

import pandas as pd
from django.db.models import Sum, Max, Min, Avg, Count
from django.core.paginator import Paginator




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
###### home resumen proyectos

class Inicio(ListView):

    def index(request):

        # Cuenta el numero de proyectos
        NoProyectos = Proyecto.objects.values('nombre').count() 
        # Cuenta el numero de proyectos sin iniciar
        NoSinIniciar = Proyecto.objects.filter(estado_id = 1).count()
        # Cuenta el numero de proyectos en proceso
        NoEnProceso = Proyecto.objects.filter(estado_id = 2).count()
        # Cuneta e numero de proyectos finalizados
        NoFinalizados = Proyecto.objects.filter(estado_id = 3).count()


        # muestra los proyectos
        proyectos = Proyecto.objects.get_queryset().order_by('estado_id')

        paginator = Paginator(proyectos,2)
        pagina = request.GET.get('page')
        proyectos = paginator.get_page(pagina)
        

        context = {
            'NoProyectos':NoProyectos,
            'NoSinIniciar':NoSinIniciar,
            'NoEnProceso':NoEnProceso,
            'NoFinalizados':NoFinalizados,
            'proyectos':proyectos,
        }
        return render(request,'home.html',context)