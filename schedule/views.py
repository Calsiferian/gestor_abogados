from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from .forms import TaskSearchForm
from datetime import date

def is_moderator(user):
    """Verifica si el usuario pertenece al grupo Moderador."""
    return user.groups.filter(name="Moderador").exists()

@login_required
def task_list(request):
  # Lógica para filtrar las tareas

    today = date.today()

    # Filtrar tareas según si el usuario es moderador o abogado
    if is_moderator(request.user):
        tasks = Task.objects.all()  # Moderadores pueden ver todas las tareas
    else:
        tasks = Task.objects.filter(abogado=request.user)  # Abogados solo ven sus tareas

    # Inicializamos el formulario con los filtros aplicados
    form = TaskSearchForm(request.GET, user=request.user)  # Pasamos el usuario al formulario

    if form.is_valid():
        abogado = form.cleaned_data.get('abogado')
        cliente_nombre = form.cleaned_data.get('cliente_nombre')
        fecha_inicio = form.cleaned_data.get('fecha_inicio')
        fecha_fin = form.cleaned_data.get('fecha_fin')

        # Filtrar tareas según los valores del formulario
        if abogado:
            tasks = tasks.filter(abogado=abogado)
        if cliente_nombre:
            tasks = tasks.filter(cliente__nombres__icontains=cliente_nombre)
        if fecha_inicio:
            tasks = tasks.filter(fecha_tarea__gte=fecha_inicio)
        if fecha_fin:
            tasks = tasks.filter(fecha_tarea__lte=fecha_fin)

        # Categorizar las tareas
        tasks_hoy = tasks.filter(fecha_tarea=today)  # Tareas para este día
        tasks_futuras = tasks.filter(fecha_tarea__gt=today)  # Tareas faltantes
        tasks_pasadas = tasks.filter(fecha_tarea__lt=today)  # Tareas pasadas

        return render(request, 'task_list.html', {
            'form': form,
            'tasks_hoy': tasks_hoy,
            'tasks_futuras': tasks_futuras,
            'tasks_pasadas': tasks_pasadas,
        })

        

@login_required
def task_create(request):
    """Crea una nueva tarea."""
    if request.method == 'POST':
        form = TaskForm(request.POST,user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.abogado = request.user
            task.save()
            return redirect('schedule:task_list')
    else:
        form = TaskForm(user=request.user)
    return render(request, 'task_create.html', {'form': form})

@login_required
def task_edit(request, pk):
    """Edita una tarea existente."""
    task = get_object_or_404(Task, pk=pk, abogado=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('schedule:task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_create.html', {'form': form})  # Reutiliza el formulario

@login_required
def task_delete(request, pk):
    """Elimina una tarea."""
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('schedule:task_list')
