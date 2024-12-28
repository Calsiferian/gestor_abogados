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
        }

    def __init__(self, *args, **kwargs):
        # Extraer el usuario de kwargs (si está presente)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)  # Llamar al constructor base de Form

        if self.user.groups.filter(name='Moderador').exists(): # Si el usuario es moderador
            self.fields['abogado'].queryset = User.objects.exclude(is_superuser=True) # Mostrar solo usuarios relevantes
            self.fields['abogado'].widget.attrs.update({'class': 'inputActualizarCliente'})
        else:  # Si no es moderador
            self.fields['abogado'].widget = forms.HiddenInput()  # Ocultamos el campo
            self.fields['abogado'].initial = self.user  # Asignamos automáticamente el usuario actual
        

class ClienteSearchForm(forms.Form):
    nombre = forms.CharField(
        required=False,  # No es obligatorio que el campo esté lleno
        label='Buscar Cliente',
        widget=forms.TextInput(attrs={'placeholder': 'Buscar por nombre cliente...', 'class': 'inputselecNombreNumero'})
    )