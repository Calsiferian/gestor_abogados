from django.db import models

class Cliente(models.Model):
    nombres = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombres