from django.db import models
from django.contrib.auth.models import User



class Cliente(models.Model):
    nombres = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    abogado = models.ForeignKey(User, related_name='clientes', on_delete=models.CASCADE)
    def __str__(self):
        return self.nombres