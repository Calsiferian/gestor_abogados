from django import forms
from .models import Payments
from clients.models import Cliente

class PaymentForm(forms.ModelForm):
    class Meta:# Configuración de metadatos del formulario. Es una convención de Django para manejar metadatos (información sobre cómo debe comportarse la clase).
        model = Payments  # Asociamos el formulario al modelo Payments
        fields = ['cliente', 'valor_pago', 'fecha_pago', 'tipo_venta', 'canal_pago']  # Campos que se incluirán en el formulario

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # Extraemos el usuario que inició sesión (pasado desde la vista)
        super().__init__(*args, **kwargs)  # Inicializamos el formulario con el método de la clase base
        # Filtramos el campo 'cliente' para que solo muestre los clientes asociados al abogado actual
        self.fields['cliente'].queryset = Cliente.objects.filter(abogado=user)
