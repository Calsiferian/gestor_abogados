from django import forms
from .models import Cliente
from django.contrib.auth.models import User

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombres', 'telefono', 'abogado']
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'inputActualizarCliente'}),
            'telefono': forms.TextInput(attrs={'class': 'inputActualizarCliente'}),
            'abogado': forms.Select(attrs={'class': 'inputActualizarCliente'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Obtener el usuario desde la vista
        super().__init__(*args, **kwargs)

        # Si el usuario es un moderador, permitir seleccionar abogados
        if user and user.groups.filter(name='Moderador').exists():
            self.fields['abogado'].queryset = User.objects.exclude(is_superuser=True)  # Mostrar todos los usuarios excepto el superusuario
        else:
            # Si no es moderador, asignar al usuario actual como abogado
            self.fields['abogado'].queryset = User.objects.filter(username=user.username)  # Solo mostrar el usuario actual
            self.fields['abogado'].required = False  # Hacer que el campo no sea obligatorio si no es moderador

    def clean_abogado(self):
        abogado = self.cleaned_data.get('abogado')
        if not abogado:  # Si no se selecciona un abogado
            return None  # Retornar None si no se selecciona un abogado
        return abogado

class ClienteSearchForm(forms.Form):
    nombre = forms.CharField(
        required=False,  # No es obligatorio que el campo esté lleno
        label='Buscar Cliente',
        widget=forms.TextInput(attrs={'placeholder': 'Buscar por nombre cliente...', 'class': 'inputselecNombreNumero'})
    )