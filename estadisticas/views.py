from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from reportes.models import Reporte


@login_required
def vista_estadisticas(request):

    # Totales por estado
    por_estado = Reporte.objects.values('estado').annotate(total=Count('id'))
    datos_estado = {item['estado']: item['total'] for item in por_estado}

    # Totales por categoría
    por_categoria = Reporte.objects.values('categoria').annotate(total=Count('id'))
    datos_categoria = {item['categoria']: item['total'] for item in por_categoria}

    # Totales por prioridad
    por_prioridad = Reporte.objects.values('prioridad').annotate(total=Count('id'))
    datos_prioridad = {item['prioridad']: item['total'] for item in por_prioridad}

    # Reportes por mes (últimos 6 meses)
    from django.utils import timezone
    from datetime import timedelta

    hoy = timezone.now()
    meses = []
    for i in range(5, -1, -1):
        fecha = hoy - timedelta(days=i * 30)
        meses.append(fecha.strftime('%b %Y'))

    # Resumen general
    total = Reporte.objects.count()
    resueltos = Reporte.objects.filter(estado='resuelto').count()
    pendientes = Reporte.objects.filter(estado='pendiente').count()
    en_proceso = Reporte.objects.filter(estado='en_proceso').count()
    tasa_resolucion = round((resueltos / total * 100), 1) if total > 0 else 0

    contexto = {
        # Para las tarjetas
        'total': total,
        'resueltos': resueltos,
        'pendientes': pendientes,
        'en_proceso': en_proceso,
        'tasa_resolucion': tasa_resolucion,

        # Para las gráficas (como JSON)
        'labels_estado': list(datos_estado.keys()),
        'datos_estado': list(datos_estado.values()),

        'labels_categoria': list(datos_categoria.keys()),
        'datos_categoria': list(datos_categoria.values()),

        'labels_prioridad': list(datos_prioridad.keys()),
        'datos_prioridad': list(datos_prioridad.values()),

        'labels_meses': meses,

        'prioridad_zip': zip(
        list(datos_prioridad.keys()),
        list(datos_prioridad.values())
    ),
    }
    return render(request, 'estadisticas/estadisticas.html', contexto)