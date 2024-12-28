from django import forms
from .models import Payments
from clients.models import Cliente
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payments  # Asociamos el formulario al modelo Payments
        fields = ['comprobante','cliente', 'valor_pago', 'fecha_pago', 'tipo_venta', 'canal_pago']  # Campos que se incluirán en el formulario

    def __init__(self, *args, **kwargs):
        # Extraer el usuario de kwargs (si está presente)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)  # Llamar al constructor base de Form


          ########################################################        # Agregamos la clase CSS y los placeholders a los inputs
        self.fields['cliente'].widget.attrs.update({
            'class': 'inputCrearPago'
        })
        self.fields['comprobante'].widget.attrs.update({
            'class': 'inputCrearPago'
        })
        self.fields['valor_pago'].widget.attrs.update({
            'class': 'inputCrearPago',
            'placeholder': 'Ingrese el valor del pago',
        })
        self.fields['fecha_pago'].widget.attrs.update({
            'class': 'inputCrearPago',
            'placeholder': 'AAAA-MM-DD',
        })
        self.fields['tipo_venta'].widget.attrs.update({
            'class': 'inputCrearPago'
        })
        self.fields['canal_pago'].widget.attrs.update({
            'class': 'inputCrearPago'
        })
      ################################################################## Sugerencia volver gidwets o sacar de ahí 

        if self.user.groups.filter(name='Moderador').exists(): # Si el usuario es moderador
            self.fields['cliente'].queryset = Cliente.objects.all() # Mostrar lista de todos los clientes del sistema
            
        else:  # Si no es moderador
            self.fields['cliente'].queryset = Cliente.objects.filter(abogado=user) # mostrar solo clientes del usuario
          
        

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

    

class PaymentSearchForm(forms.Form):
    abogado = forms.ModelChoiceField(
        queryset=User.objects.none(), 
        required=False, 
        widget=forms.Select(attrs={
            'class': 'inputBuscarPago'
        })
    )
    cliente_nombre = forms.CharField(
        max_length=100, 
        required=False, 
        widget=forms.TextInput(attrs={
            'class': 'inputBuscarPago',
            'placeholder': 'Buscar por nombre...'  # Placeholder agregado
        })
    )

    def __init__(self, *args, **kwargs):
        # Extraer el usuario de kwargs (si está presente)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)  # Llamar al constructor base de Form
        
        # Personalización del queryset según el tipo de usuario
        if self.user:
            # Si el usuario es moderador, mostramos todos los abogados
            if self.user.groups.filter(name='Moderador').exists():
                self.fields['abogado'].queryset = User.objects.filter(groups__name='Usuario Regular')
            # Si el usuario es un abogado, mostramos solo al mismo
            elif self.user.groups.filter(name='Usuario Regular').exists():
                self.fields['abogado'].queryset = User.objects.filter(id=self.user.id)

