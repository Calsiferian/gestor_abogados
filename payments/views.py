# payments/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from clients.models import Cliente  # Importamos el modelo Cliente de la app 'clients'
from .models import Payments  # Importamos el modelo Payments de la app 'payments'
from .forms import PaymentForm
from .forms import ClienteSearchForm

@login_required
def listar_pagos(request):
    # Verificar si el usuario tiene el rol de "moderador"
    if request.user.groups.filter(name='Moderador').exists():
        # Si es moderador, obtener todos los pagos
        pagos = Payments.objects.all()
    else:
        # Si es abogado, obtener solo los pagos de sus clientes
        clientes_abogado = Cliente.objects.filter(abogado=request.user)
        pagos = Payments.objects.filter(cliente__in=clientes_abogado)

    # Crear el formulario de búsqueda y procesarlo si se recibe un valor de búsqueda
    form = ClienteSearchForm(request.GET)  # Utiliza el mismo formulario que en listar_clientes
    if form.is_valid():
        nombre = form.cleaned_data.get('nombre')
        if nombre:
            # Filtrar los pagos por el nombre del cliente
            pagos = pagos.filter(cliente__nombres__icontains=nombre)

    # Pasar los pagos y el formulario al contexto
    return render(request, 'listar_pagos.html', {
        'pagos': pagos,
        'form': form
    })

@login_required
def crear_pago(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST, user=request.user)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.save()
            return redirect('payments:listar_pagos')
    else:
        form = PaymentForm(user=request.user)

    return render(request, 'crear_pago.html', {'form': form})

@login_required
def editar_pago(request, pk):
    pago = get_object_or_404(Payments, pk=pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=pago, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('payments:listar_pagos')
    else:
        form = PaymentForm(instance=pago, user=request.user)
    return render(request, 'editar_pago.html', {'form': form})

@login_required
def borrar_pago(request, pk):
    pago = get_object_or_404(Payments, pk=pk)
    if request.method == 'POST':
        pago.delete()
        return redirect('payments:listar_pagos')