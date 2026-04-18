from django.db import models
from usuarios.models import Usuario


class Reporte(models.Model):

    CATEGORIA_CHOICES = [
        ('vandalismo', 'Vandalismo'),
        ('calle', 'Daños en la calle'),
        ('luminaria', 'Luminaria'),
        ('propiedad_publica', 'Daño de propiedad pública'),
        ('basura', 'Acumulación de basura'),
        ('alcantarillado', 'Alcantarillado'),
        ('otro', 'Otro'),
    ]

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En proceso'),
        ('resuelto', 'Resuelto'),
        ('rechazado', 'Rechazado'),
    ]

    PRIORIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]

    titulo = models.CharField(max_length=200, verbose_name='Título')
    descripcion = models.TextField(verbose_name='Descripción')
    categoria = models.CharField(
        max_length=30, choices=CATEGORIA_CHOICES, verbose_name='Categoría'
    )
    estado = models.CharField(
        max_length=20, choices=ESTADO_CHOICES, default='pendiente', verbose_name='Estado'
    )
    prioridad = models.CharField(
        max_length=10, choices=PRIORIDAD_CHOICES, default='media', verbose_name='Prioridad'
    )
    direccion = models.CharField(max_length=300, verbose_name='Dirección aproximada')
    latitud = models.FloatField(verbose_name='Latitud')
    longitud = models.FloatField(verbose_name='Longitud')
    foto_evidencia = models.ImageField(
        upload_to='reportes/', blank=True, null=True, verbose_name='Foto de evidencia'
    )
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE,
        related_name='reportes', verbose_name='Ciudadano'
    )
    fecha_reporte = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de reporte')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    comentario_admin = models.TextField(
        blank=True, null=True, verbose_name='Comentario del administrador'
    )

    class Meta:
        verbose_name = 'Reporte'
        verbose_name_plural = 'Reportes'
        ordering = ['-fecha_reporte']

    def __str__(self):
        return f'{self.titulo} — {self.get_estado_display()}'

    @property
    def color_estado(self):
        colores = {
            'pendiente': 'warning',
            'en_proceso': 'info',
            'resuelto': 'success',
            'rechazado': 'danger',
        }
        return colores.get(self.estado, 'secondary')

    @property
    def icono_categoria(self):
        iconos = {
            'vandalismo': 'bi-exclamation-triangle',
            'calle': 'bi-cone-striped',
            'luminaria': 'bi-lightbulb',
            'propiedad_publica': 'bi-building',
            'basura': 'bi-trash',
            'alcantarillado': 'bi-droplet',
            'otro': 'bi-question-circle',
        }
        return iconos.get(self.categoria, 'bi-flag')