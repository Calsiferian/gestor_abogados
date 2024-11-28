# Importación de funciones necesarias de Django
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login

# Vista de inicio de sesión
def login_view(request):
    # Verifica si la solicitud es de tipo POST (es decir, cuando el usuario envía el formulario)
    if request.method == 'POST':
        # Crea una instancia del formulario de autenticación con los datos enviados en el POST
        form = AuthenticationForm(request, data=request.POST)
        
        # Si el formulario es válido, es decir, las credenciales pasaron la validación
        if form.is_valid():
            # Extrae el nombre de usuario y la contraseña del formulario
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Intenta autenticar al usuario con el nombre de usuario y la contraseña
            user = authenticate(request, username=username, password=password)
            
            # Si el usuario fue autenticado correctamente (es decir, las credenciales son válidas)
            if user is not None:
                # Inicia sesión para el usuario autenticado
                login(request, user)
                
                # Verifica si el usuario es un superusuario (administrador)
                if user.is_superuser:
                    # Si es superusuario, redirige al panel de administración
                    return redirect('admin:index')
                
                # Si no es superusuario, redirige a la página de inicio u otra página configurada
                return redirect('/clients')  #  es el nombre de la URL de la página de inicio
                
            else:
                # Si el usuario no fue encontrado (credenciales incorrectas), añade un error al formulario
                form.add_error(None, 'Credenciales incorrectas')
        
        # Si el formulario no es válido, añade un error al formulario
        else:
           form.add_error(None, 'Datos no validos') 
    
    # Si la solicitud es GET (cuando se carga la página inicial de inicio de sesión), crea un formulario vacío
    else:
        form = AuthenticationForm()

    # Renderiza la plantilla 'login.html' y pasa el formulario al contexto
    return render(request, 'login.html', {'form': form})
