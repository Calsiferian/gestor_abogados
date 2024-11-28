from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cliente
from .forms import ClienteForm
from django.contrib import messages

# Vista para listar clientes
@login_required
def listar_clientes(request):
    # Verificar si el usuario tiene el rol de "moderador"
    if request.user.groups.filter(name='Moderador').exists():
        # Si es moderador, obtener todos los clientes
        clientes = Cliente.objects.all()
    else:
        # Si es abogado, obtener solo los clientes asociados a él
        clientes = Cliente.objects.filter(abogado=request.user)

    return render(request, 'listar_clientes.html', {'clientes': clientes})

# Vista para crear un cliente
@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)  # No guardar aún
            cliente.abogado = request.user  # Asignar al abogado (usuario actual)
            cliente.save()  # Ahora guardar el cliente
            return redirect('clients:list_clients')
    else:
        form = ClienteForm()
    return render(request, 'crear_cliente.html', {'form': form})

# Vista para actualizar un cliente
@login_required
def actualizar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clients:list_clients') 
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'update_client.html', {'form': form, 'actualizar': True})

# Vista para borrar un cliente
@login_required
def borrar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.user.groups.filter(name='Moderador').exists():
        cliente.delete()
        return redirect('clients:list_clients')
    else:
        messages.error(request, 'No tienes permiso para eliminar clientes. Comunicate con un administrador del sistema')
        return redirect('clients:list_clients')