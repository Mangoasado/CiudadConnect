from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El correo electrónico es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', 'administrador')
        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractUser):
    ROL_CHOICES = [
        ('ciudadano', 'Ciudadano'),
        ('administrador', 'Administrador'),
    ]

    username = None
    email = models.EmailField(unique=True, verbose_name='Correo electrónico')
    nombre_completo = models.CharField(max_length=200, verbose_name='Nombre completo')
    numero_identificacion = models.CharField(
        max_length=20, unique=True, verbose_name='Número de identificación'
    )
    foto_perfil = models.ImageField(
        upload_to='perfiles/', blank=True, null=True, verbose_name='Foto de perfil'
    )
    telefono = models.CharField(max_length=15, blank=True, verbose_name='Teléfono')
    direccion = models.CharField(max_length=300, blank=True, verbose_name='Dirección')
    rol = models.CharField(
        max_length=20, choices=ROL_CHOICES, default='ciudadano', verbose_name='Rol'
    )
    notificaciones_email = models.BooleanField(
        default=True, verbose_name='Recibir notificaciones por correo'
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre_completo', 'numero_identificacion']

    objects = UsuarioManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f'{self.nombre_completo} ({self.email})'

    @property
    def es_administrador(self):
        return self.rol == 'administrador'