# payments/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from clients.models import Cliente  # Importamos el modelo Cliente de la app 'clients'
from .models import Payments  # Importamos el modelo Payments de la app 'payments'
from .forms import PaymentForm

@login_required
def listar_pagos(request):
    #Obtener el abogado logueado
    abogado = request.user  # Esto es el User (abogado) logueado

    # Filtrar los clientes del abogado
    clientes_abogado = Cliente.objects.filter(abogado=abogado)

    # Filtrar los pagos de los clientes de ese abogado
    pagos = Payments.objects.filter(cliente__in=clientes_abogado)

    return render(request, 'listar_pagos.html', {'pagos': pagos})

@login_required
def crear_pago(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST, user=request.user)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.save()
            return redirect('listar_pagos')
    else:
        form = PaymentForm(user=request.user)

    return render(request, 'crear_pago.html', {'form': form})