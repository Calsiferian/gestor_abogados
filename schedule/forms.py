from django import forms
from .models import Task
from django.contrib.auth.models import User


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['cliente', 'tarea', 'fecha_tarea']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'inputActualizarCliente'}),
            'tarea': forms.TextInput(attrs={'class': 'inputTarea', 'placeholder': 'Descripción de la tarea'}),
            'fecha_tarea': forms.DateInput(
                attrs={'class': 'inputActualizarCliente', 'type': 'date', 'placeholder': 'Selecciona una fecha'}
            ),
        }


#class TaskForm(forms.ModelForm):
#    class Meta:
#        model = Task
#        fields = ['cliente',  'tarea', 'fecha_tarea']


class TaskSearchForm(forms.Form):
    abogado = forms.ModelChoiceField(
        queryset=User.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'inputsCrearNuevaTarea'})
    )
    cliente_nombre = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'inputsCrearNuevaTarea', 'placeholder': 'Nombre del cliente...'})
    )
    
    def __init__(self, *args, **kwargs):
        # Extraer el usuario de kwargs (si está presente)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)  # Llamar al constructor base de Form

        # Personalización del formulario según el tipo de usuario
        if self.user:
            # Si el usuario es moderador, mostramos todos los abogados
            if self.user.groups.filter(name='Moderador').exists():
                self.fields['abogado'].queryset = User.objects.filter(groups__name='Usuario Regular')
            
            # Si el usuario es un abogado, mostramos solo el mismo
            elif self.user.groups.filter(name='Usuario Regular').exists():
                self.fields['abogado'].queryset = User.objects.filter(id=self.user.id)
