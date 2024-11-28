from django import forms
from .models import Payments
from clients.models import Cliente
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payments  # Asociamos el formulario al modelo Payments
        fields = ['cliente', 'valor_pago', 'fecha_pago', 'tipo_venta', 'canal_pago']  # Campos que se incluirán en el formulario

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # Extraemos el usuario que inició sesión (pasado desde la vista)
        super().__init__(*args, **kwargs)  # Inicializamos el formulario con el método de la clase base
        # Filtramos el campo 'cliente' para que solo muestre los clientes asociados al abogado actual
        self.fields['cliente'].queryset = Cliente.objects.filter(abogado=user)

    # Validación para asegurarnos de que el valor_pago sea un número entero positivo
    def clean_valor_pago(self):
        valor_pago = self.cleaned_data.get('valor_pago')
        if valor_pago <= 0:
            raise ValidationError("El valor del pago debe ser un número positivo.")
        return valor_pago

    # Validación para asegurarnos de que la fecha esté en formato correcto (YYYY-MM-DD)
    def clean_fecha_pago(self):
        fecha_pago = self.cleaned_data.get('fecha_pago')
        if fecha_pago:
            try:
                # Convertimos la fecha a formato de fecha en caso de que no sea válida
                fecha_formateada = parse_date(str(fecha_pago))
                if not fecha_formateada:
                    raise ValidationError("La fecha debe estar en formato AAAA-MM-DD.")
            except ValueError:
                raise ValidationError("La fecha debe estar en formato AAAA-MM-DD.")
        return fecha_pago
    
class ClienteSearchForm(forms.Form):
    nombre = forms.CharField(required=False, label="Buscar Pago Cliente")
