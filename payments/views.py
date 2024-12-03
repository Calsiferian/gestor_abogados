# payments/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from clients.models import Cliente  # Importamos el modelo Cliente de la app 'clients'
from .models import Payments  # Importamos el modelo Payments de la app 'payments'
from .forms import PaymentForm
from .forms import PaymentSearchForm

@login_required
def listar_pagos(request):
    """
    Vista para listar y filtrar pagos:
    - Moderadores: pueden ver todos los pagos y filtrar por abogado.
    - Abogados: solo pueden ver los pagos de sus clientes.
    """

    # Verificar si el usuario tiene el rol de "moderador"
    if request.user.groups.filter(name='Moderador').exists():
        # Si es moderador, obtener todos los pagos
        pagos = Payments.objects.all()
        es_moderador = True
    else:
        # Si es abogado, obtener solo los pagos de sus clientes
        clientes_abogado = Cliente.objects.filter(abogado=request.user)
        pagos = Payments.objects.filter(cliente__in=clientes_abogado)
        es_moderador = False

    # Crear el formulario de búsqueda (incluye abogado solo si es moderador)
    form = PaymentSearchForm(request.GET, user=request.user)  # Asegúrate de pasar el usuario )

    # Procesar el formulario si es válido
    if form.is_valid():
        cliente_nombre = form.cleaned_data.get('cliente_nombre')  # Filtro por nombre del cliente
        abogado = form.cleaned_data.get('abogado')  # Filtro por abogado (solo moderadores)

        if cliente_nombre:
            # Filtrar los pagos por el nombre del cliente
            pagos = pagos.filter(cliente__nombres__icontains=cliente_nombre)

        if es_moderador and abogado:
            # Filtrar por abogado (solo si el usuario es moderador)
            pagos = pagos.filter(cliente__abogado=abogado)

    # Renderizar la plantilla con los datos y el formulario
    return render(request, 'listar_pagos.html', {
        'pagos': pagos,  # Lista filtrada de pagos
        'form': form  # Formulario de búsqueda
        
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