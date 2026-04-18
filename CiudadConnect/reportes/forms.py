from django import forms
from .models import Reporte


class FormularioReporte(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = [
            'titulo', 'descripcion', 'categoria',
            'prioridad', 'latitud',
            'longitud', 'foto_evidencia'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Hueco en la vía principal',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe el problema con el mayor detalle posible...',
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select',
            }),
            'prioridad': forms.Select(attrs={
                'class': 'form-select',
            }),
            'latitud': forms.HiddenInput(),
            'longitud': forms.HiddenInput(),
            'foto_evidencia': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
        }
        labels = {
            'titulo': 'Título del reporte',
            'descripcion': 'Descripción detallada',
            'categoria': 'Categoría',
            'prioridad': 'Prioridad',
            'foto_evidencia': 'Foto de evidencia (opcional)',
        }

class FormularioEditarReporte(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = [
            'titulo', 'descripcion', 'categoria',
            'prioridad', 'latitud', 'longitud', 'foto_evidencia'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select',
            }),
            'prioridad': forms.Select(attrs={
                'class': 'form-select',
            }),
            'latitud': forms.HiddenInput(),
            'longitud': forms.HiddenInput(),
            'foto_evidencia': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
        }