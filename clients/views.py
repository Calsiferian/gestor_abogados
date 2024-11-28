from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente
from .forms import ClienteForm

# Vista para listar clientes
def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'listar_clientes.html', {'clientes': clientes})

# Vista para crear un cliente
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_clients')
    else:
        form = ClienteForm()
    return render(request, 'crear_cliente.html', {'form': form})

# Vista para actualizar un cliente
def actualizar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('list_clients') ## TO DO vista de actualizar cliente. 
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'update_client.html', {'form': form, 'actualizar': True})

# Vista para borrar un cliente
def borrar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.delete()
    return redirect('list_clients')