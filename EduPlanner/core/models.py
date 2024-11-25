from django.db import models

# Create your models here.

class Evento(models.Model):
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    tipo = models.CharField(max_length=50)
    aprobado = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo
    
class Feriado(models.Model):
    nombre = models.CharField(max_length=150)
    fecha = models.DateField()
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} ({self.fecha})"
    