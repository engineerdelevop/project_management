from django.contrib.auth.forms import AuthenticationForm
# importar libreria de forms
from django import forms
from django.forms import fields, widgets
# importar los modelos
from .models import *

# Se debe instalar pip install django-crispy-forms


class FormularioLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(FormularioLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'


class FormsProyecto(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = '__all__'
        widgets = {'fecha_inicial': forms.DateInput(attrs={'type':'date'}), 'fecha_final': forms.DateInput(attrs={'type':'date'})}
        # widgets = {'fecha_final': forms.DateInput(attrs={'type':'date'})}

class FormsProyectoActualizar(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = '__all__'
        exclude = ['slug', ]
        widgets = {'fecha_inicial': forms.DateInput(attrs={'type':'date'}), 'fecha_final': forms.DateInput(attrs={'type':'date'})}
        # widgets = {'fecha_final': forms.DateInput(attrs={'type':'date'})}

class FormsCrearActividades(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = '__all__'
        #exclude = ['proyecto', ]
        widgets = {'fecha_inicial': forms.DateInput(attrs={'type':'date'}), 'fecha_final': forms.DateInput(attrs={'type':'date'})}

class FormsActualizarActividades(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = '__all__'
        exclude = ['proyecto', ]
        widgets = {'fecha_inicial': forms.DateInput(attrs={'type':'date'}), 'fecha_final': forms.DateInput(attrs={'type':'date'})}

class FormsActualizarActividadesTrabajador(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = '__all__'
        exclude = ['proyecto', 'fase', 'nombre_actividad', 'descripcion', 'responsable' , 'fecha_inicial' ,'fecha_final']
        #widgets = {'fecha_inicial': forms.DateInput(attrs={'type':'date'}), 'fecha_final': forms.DateInput(attrs={'type':'date'})}

