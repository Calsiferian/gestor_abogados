# pagos/models.py
from django.db import models
from clients.models import Cliente  # Importamos el modelo Cliente desde la aplicación 'clientes'

class Payments(models.Model):
    # Asociamos cada pago a un cliente
    comprobante = models.IntegerField()  # comprobante
    cliente = models.ForeignKey(Cliente, related_name='paymets', on_delete=models.CASCADE)
    
    # Campos adicionales
    valor_pago = models.IntegerField()  # Valor del pago en número entero
    fecha_pago = models.DateField()  # Fecha del pago
    TIPO_VENTA_CHOICES = [
        ('mini', 'Mini'),
        ('nueva', 'Nueva'),
        ('cuota', 'Cuota'),
    ]
    tipo_venta = models.CharField(max_length=5, choices=TIPO_VENTA_CHOICES)
    
    CANAL_PAGO_CHOICES = [
        ('nequi', 'Nequi'),
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia Bancaria'),
    ]
    canal_pago = models.CharField(max_length=15, choices=CANAL_PAGO_CHOICES)

    def __str__(self):
        return f"Pago de {self.cliente.nombres} - {self.valor_pago} en {self.fecha_pago}"
