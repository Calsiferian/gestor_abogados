from django import forms
from payments.models import Payments
from django.contrib.auth.models import User


class TariffingFilterForm(forms.Form):
    fecha_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'inputBuscarPago',
                'placeholder': 'Selecciona la fecha de inicio'
            }
        ),
        label="Fecha de Inicio"
    )
    fecha_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'inputBuscarPago',
                'placeholder': 'Selecciona la fecha de fin'
            }
        ),
        label="Fecha de Fin"
    )
    canal = forms.ChoiceField(
        required=False,
        choices=[('', 'Todos')] + Payments.CANAL_PAGO_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'inputBuscarPago',
                'placeholder': 'Selecciona un canal de pago'
            }
        ),
        label="Canal de Pago"
    )
    abogado = forms.ModelChoiceField(
        required=False,
        queryset=User.objects.filter(groups__name='Usuario Regular'),
        widget=forms.Select(
            attrs={
                'class': 'inputBuscarPago',
                'placeholder': 'Selecciona un abogado'
            }
        ),
        label="Abogado"
    )
