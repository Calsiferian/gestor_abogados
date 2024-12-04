from django.db import models
from django.contrib.auth.models import User
from clients.models import Cliente  # Ajusta el import según el nombre de tu app de clientes

class Task(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='tasks')
    tarea = models.TextField()
    fecha_tarea = models.DateField()
    abogado = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    creada_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Task for {self.cliente} - {self.tarea[:20]}"

    class Meta:
        ordering = ['fecha_tarea']
