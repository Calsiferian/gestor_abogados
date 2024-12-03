from django import forms
from payments.models import Payments
from django.contrib.auth.models import User


class TariffingFilterForm(forms.Form):
    fecha_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Fecha de Inicio"
    )
    fecha_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Fecha de Fin"
    )
    canal = forms.ChoiceField(
        required=False,
        choices=[('', 'Todos')] + Payments.CANAL_PAGO_CHOICES,
        label="Canal de Pago"
    )
    abogado = forms.ModelChoiceField(
        required=False,
        queryset= User.objects.filter(groups__name='Usuario Regular'),
        label="Abogado"
    )
