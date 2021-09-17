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

# resumen principal

import pandas as pd
from django.db.models import Sum, Max, Min, Avg



# Create your views here.


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


class Inicio(ListView):

    def index(request):

        # contar No de proyectos
        # No_proyectos = Proyecto.objects.filter().count()

        # dataframe, don include the join tables

        # df = pd.DataFrame(list(Proyecto.objects.all().values()))
            
        # select one part of the database

        #labels = []
        #data = []
        #queryset5 = Proyecto.objects.values('estado__nombre').annotate(No_estado=Count('presupuesto')).order_by('-estado')

        # SQL conection
        
        #SQL2 = Proyecto.objects.raw("SELECT 1 as id, base_proyecto.estado_id, base_estado.nombre, COUNT( base_estado.nombre) AS ['total'] FROM base_proyecto INNER JOIN base_estado ON base_estado.id = base_proyecto.estado_id GROUP BY base_proyecto.estado_id")

        #df2 = pd.DataFrame(list(Proyecto.objects.raw("SELECT 1 as id, base_proyecto.estado_id, base_estado.nombre, COUNT( base_estado.nombre) AS ['Total'] FROM base_proyecto INNER JOIN base_estado ON base_estado.id = base_proyecto.estado_id GROUP BY base_proyecto.estado_id")))

        #for i in SQL2:
        #    labels.append(i.nombre)
        #    print(i)
        
        context = {
            #'No_proyectos': No_proyectos,
            #'Resultado':queryset5,
        }

        # print(labels)
        return render(request,'home.html',context)