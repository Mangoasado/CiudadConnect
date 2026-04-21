from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Usuario


class FormularioLogin(AuthenticationForm):
    username = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'tu@correo.com',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '••••••••',
        })
    )


class FormularioRegistro(UserCreationForm):
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'tu@correo.com',
        })
    )
    nombre_completo = forms.CharField(
        label='Nombre completo',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Juan Pérez',
        })
    )
    numero_identificacion = forms.CharField(
        label='Número de identificación',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '1234567890',
        })
    )
    telefono = forms.CharField(
        label='Teléfono',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '3001234567',
        })
    )
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '••••••••',
        })
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '••••••••',
        })
    )

    class Meta:
        model = Usuario
        fields = [
            'email', 'nombre_completo', 'numero_identificacion',
            'telefono', 'password1', 'password2'
        ]


class FormularioPerfil(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'nombre_completo', 'numero_identificacion', 'telefono',
            'direccion', 'foto_perfil', 'notificaciones_email'
        ]
        widgets = {
            'nombre_completo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu nombre completo',
            }),
            'numero_identificacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '1234567890',
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '3001234567',
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu dirección',
            }),
            'foto_perfil': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
            'notificaciones_email': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
        labels = {
            'nombre_completo': 'Nombre completo',
            'numero_identificacion': 'Número de identificación',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
            'foto_perfil': 'Foto de perfil',
            'notificaciones_email': 'Recibir notificaciones por correo',
        }