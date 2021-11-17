from django.contrib import admin
from .models import *

#Se agrega permision

# from django.contrib.auth

# Register your models here.

admin.site.register(TipoProyecto)
admin.site.register(Responsable)
admin.site.register(Cliente)
admin.site.register(Estado)
admin.site.register(Proyecto)
admin.site.register(FaseProyecto)
admin.site.register(Actividad)

