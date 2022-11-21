from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
# class User(models.Model):
#     Correo = models.EmailField()
#     Contrasena = models.CharField(max_length=30)


class Vuelo(models.Model):
    Usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    Aerolinea = models.CharField(max_length=30)
    Salida = models.CharField(max_length=30)
    Llegada = models.CharField(max_length=30)
    Tiempo_salida = models.DateTimeField()
    Tiempo_llegada = models.DateTimeField()
    Maletas = models.PositiveSmallIntegerField()
    Asiento = models.CharField(max_length=5)
