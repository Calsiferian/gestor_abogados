from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombres', 'telefono']
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'inputActualizarCliente'}),
            'telefono': forms.TextInput(attrs={'class': 'inputActualizarCliente'}),
        }

class ClienteSearchForm(forms.Form):
    nombre = forms.CharField(
        required=False,  # No es obligatorio que el campo esté lleno
        label='Buscar Cliente',
        widget=forms.TextInput(attrs={'placeholder': 'Buscar por nombre cliente...', 'class': 'inputselecNombreNumero'})
    )