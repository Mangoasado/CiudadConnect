from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from reportes.models import Reporte


@login_required
def vista_mapa(request):
    reportes = Reporte.objects.exclude(latitud=None, longitud=None)

    # Construir lista de marcadores para pasarla al template
    marcadores = []
    for reporte in reportes:
        marcadores.append({
            'id': reporte.id,
            'titulo': reporte.titulo,
            'categoria': reporte.get_categoria_display(),
            'estado': reporte.get_estado_display(),
            'color_estado': reporte.color_estado,
            'direccion': reporte.direccion,
            'lat': reporte.latitud,
            'lng': reporte.longitud,
            'icono': reporte.icono_categoria,
            'fecha': reporte.fecha_reporte.strftime('%d/%m/%Y'),
            'url': f'/reportes/{reporte.id}/',
        })

    contexto = {
        'marcadores': marcadores,
        'google_maps_key': settings.GOOGLE_MAPS_API_KEY,
        'total_reportes': reportes.count(),
    }
    return render(request, 'mapa/mapa.html', contexto)