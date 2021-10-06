from django.db import models

# Create your models here.

class ModeloBase(models.Model):
    id = models.AutoField(primary_key=True)
    estado = models.BooleanField('Estado', default=True)
    fecha_creacion = models.DateField('Fecha de creación', auto_now=False ,auto_now_add=True)
    fecha_modificacion = models.DateField('Fecha de modificación', auto_now=True, auto_now_add=False)
    fecha_eliminacion = models.DateField('Fecha de eliminación', auto_now=True, auto_now_add=False)

    class  Meta:
        abstract = True


class TipoProyecto(ModeloBase):
    nombre = models.CharField('Nombre tipo proyecto', max_length=100, unique=True)

    class Meta:
        verbose_name = 'tipo'
        verbose_name_plural = 'Tipos'

    def __str__(self):
        return self.nombre


class Responsable(ModeloBase):
    nombre = models.CharField('Nombres', max_length=150)
    apellidos = models.CharField('Apellidos', max_length=120)
    cargo = models.CharField('Cargo', max_length=150)
    email = models.EmailField('Correo electronico', max_length=200, unique = True) 
    descripcion = models.TextField('Descripción')

    class  Meta:
        verbose_name = 'Responsable'
        verbose_name_plural = 'Responsables'

    def __str__(self):
        return '{0} {1}'.format(self.nombre,self.apellidos)


class Cliente(ModeloBase):
    nombreCliente = models.CharField('Nombre cliente', max_length=150, unique=True)

    class  Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.nombreCliente


class Estado(ModeloBase):
    nombre = models.CharField('Nombre estado', max_length=150 ,unique=True)

    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'

    def __str__(self):
        return self.nombre


class Proyecto(ModeloBase):
    nombre = models.CharField('Nombre proyecto', max_length=150, unique=True)
    slug = models.CharField('Slug', max_length=150, unique=True, null=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoProyecto, on_delete=models.CASCADE)
    objetivo = models.TextField('Objetivo')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    presupuesto = models.FloatField('Presupuesto')
    presupuesto_ejecutado = models.FloatField('Presupuesto ejecutado', null=True)
    numero_activdades = models.IntegerField('Número de activiades', null=True)
    fecha_inicial = models.DateField('Fecha inicio')
    fecha_final = models.DateField('Fecha fin')
    responsable = models.ForeignKey(Responsable, on_delete=models.CASCADE)


class FaseProyecto(ModeloBase):
    nombre = models.CharField('Nombre de la fase', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Fase'
        verbose_name_plural = 'Fases'

    def __str__(self):
        return self.nombre


class Actividad(ModeloBase):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    fase = models.ForeignKey(FaseProyecto, on_delete=models.CASCADE)
    nombre_actividad = models.CharField('Nombre de actividad', max_length=150)
    descripcion = models.TextField('Descripción de la actividad')
    meta = models.IntegerField('Meta')
    avance = models.IntegerField('Avance', null=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    responsable = models.ForeignKey(Responsable, on_delete=models.CASCADE, null= True)
    fecha_inicial = models.DateField('Fecha inicio')
    fecha_final = models.DateField('Fecha fin')


    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'

    def __str__(self):
        return self.nombre_actividad









