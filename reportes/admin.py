from django.contrib import admin
from .models import Reporte


@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'categoria', 'estado', 'prioridad', 'usuario', 'fecha_reporte']
    list_filter = ['estado', 'categoria', 'prioridad']
    search_fields = ['titulo', 'descripcion', 'direccion', 'usuario__nombre_completo']
    ordering = ['-fecha_reporte']
    readonly_fields = ['fecha_reporte', 'fecha_actualizacion']