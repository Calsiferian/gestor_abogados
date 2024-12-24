from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'inputForm',  # Agrega tu clase CSS
            'placeholder': 'Usuario',  # Agrega un placeholder
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'inputForm',  # Agrega tu clase CSS
            'placeholder': 'Contraseña',  # Agrega un placeholder
        })
    )


#class LoginForm(AuthenticationForm):
#    username = forms.CharField(max_length=100)
#    password = forms.CharField(widget=forms.PasswordInput)