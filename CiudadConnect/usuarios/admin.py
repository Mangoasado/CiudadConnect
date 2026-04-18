from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ['email', 'nombre_completo', 'rol', 'is_active', 'fecha_registro']
    list_filter = ['rol', 'is_active', 'is_staff']
    search_fields = ['email', 'nombre_completo', 'numero_identificacion']
    ordering = ['-fecha_registro']

    fieldsets = (
        ('Acceso', {'fields': ('email', 'password')}),
        ('Información personal', {
            'fields': ('nombre_completo', 'numero_identificacion', 'foto_perfil',
                       'telefono', 'direccion')
        }),
        ('Rol y permisos', {
            'fields': ('rol', 'is_active', 'is_staff', 'is_superuser', 'groups',
                       'user_permissions')
        }),
        ('Preferencias', {'fields': ('notificaciones_email',)}),
    )

    add_fieldsets = (
        ('Crear usuario', {
            'classes': ('wide',),
            'fields': ('email', 'nombre_completo', 'numero_identificacion',
                       'rol', 'password1', 'password2'),
        }),
    )