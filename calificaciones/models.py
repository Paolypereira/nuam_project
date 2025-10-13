from django.db import models
from django.contrib.auth.models import User

class InstrumentoNoInscrito(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class CalificacionTributaria(models.Model):
    tipo = models.CharField(max_length=50)
    monto = models.DecimalField(max_digits=20, decimal_places=2)
    factor = models.DecimalField(max_digits=10, decimal_places=4)
    fecha = models.DateField()
    fuente = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    instrumento = models.ForeignKey(InstrumentoNoInscrito, on_delete=models.CASCADE, related_name='calificaciones')

    def __str__(self):
        return f'{self.tipo} - {self.fecha}'

class HistorialCambio(models.Model):
    calificacion = models.ForeignKey(CalificacionTributaria, on_delete=models.CASCADE, related_name='historial_cambios')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tipo_cambio = models.CharField(max_length=50)
    fecha = models.DateTimeField(auto_now_add=True)
    detalles = models.TextField(blank=True)

    def __str__(self):
        return f'{self.tipo_cambio} - {self.fecha}'

class ArchivoCargaMasiva(models.Model):
    nombre = models.CharField(max_length=255)
    formato = models.CharField(max_length=10)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
