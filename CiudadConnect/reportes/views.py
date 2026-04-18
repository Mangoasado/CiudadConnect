from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Reporte
from .forms import FormularioReporte


@login_required
def lista_reportes(request):
    if request.user.es_administrador:
        reportes = Reporte.objects.all()
    else:
        reportes = Reporte.objects.filter(usuario=request.user)

    estado = request.GET.get('estado')
    categoria = request.GET.get('categoria')

    if estado:
        reportes = reportes.filter(estado=estado)
    if categoria:
        reportes = reportes.filter(categoria=categoria)

    contexto = {
        'reportes': reportes,
        'estado_actual': estado,
        'categoria_actual': categoria,
        'estados': Reporte.ESTADO_CHOICES,
        'categorias': Reporte.CATEGORIA_CHOICES,
    }
    return render(request, 'reportes/lista.html', contexto)


@login_required
def nuevo_reporte(request):
    if request.method == 'POST':
        form = FormularioReporte(request.POST, request.FILES)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.usuario = request.user
            reporte.save()
            messages.success(request, '¡Reporte enviado exitosamente!')
            return redirect('lista_reportes')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = FormularioReporte()

    return render(request, 'reportes/nuevo.html', {
        'form': form,
        'google_maps_key': settings.GOOGLE_MAPS_API_KEY,
    })


@login_required
def detalle_reporte(request, pk):
    # Cualquier usuario autenticado puede ver cualquier reporte
    reporte = get_object_or_404(Reporte, pk=pk)

    return render(request, 'reportes/detalle.html', {
        'reporte': reporte,
        'google_maps_key': settings.GOOGLE_MAPS_API_KEY,
        'estados': Reporte.ESTADO_CHOICES,
    })


@login_required
def actualizar_estado(request, pk):
    if not request.user.es_administrador:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('lista_reportes')

    reporte = get_object_or_404(Reporte, pk=pk)

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        comentario = request.POST.get('comentario_admin', '')

        if nuevo_estado in dict(Reporte.ESTADO_CHOICES):
            reporte.estado = nuevo_estado
            reporte.comentario_admin = comentario
            reporte.save()
            messages.success(request, f'✓ Estado actualizado correctamente a: {reporte.get_estado_display()}')
        else:
            messages.error(request, 'Estado inválido.')

    return redirect('detalle_reporte', pk=pk)

@login_required
def eliminar_reporte(request, pk):
    if request.user.es_administrador:
        reporte = get_object_or_404(Reporte, pk=pk)
    else:
        reporte = get_object_or_404(Reporte, pk=pk, usuario=request.user)

    if request.method == 'POST':
        reporte.delete()
        messages.success(request, f'Reporte eliminado correctamente.')
        return redirect('lista_reportes')

    return render(request, 'reportes/confirmar_eliminar.html', {'reporte': reporte})

@login_required
def editar_reporte(request, pk):
    # Solo el dueño o el admin pueden editar
    if request.user.es_administrador:
        reporte = get_object_or_404(Reporte, pk=pk)
    else:
        reporte = get_object_or_404(Reporte, pk=pk, usuario=request.user)

    # Ciudadano no puede editar si ya está en proceso o resuelto
    if not request.user.es_administrador and reporte.estado in ['en_proceso', 'resuelto', 'rechazado']:
        messages.error(request, 'No puedes editar un reporte que ya está siendo gestionado.')
        return redirect('detalle_reporte', pk=pk)

    from .forms import FormularioEditarReporte

    if request.method == 'POST':
        form = FormularioEditarReporte(request.POST, request.FILES, instance=reporte)
        if form.is_valid():
            form.save()
            messages.success(request, f'Reporte #{pk} actualizado correctamente.')
            return redirect('detalle_reporte', pk=pk)
        else:
            messages.error(request, 'Por favor corrige los errores.')
    else:
        form = FormularioEditarReporte(instance=reporte)

    return render(request, 'reportes/editar.html', {
        'form': form,
        'reporte': reporte,
        'google_maps_key': settings.GOOGLE_MAPS_API_KEY,
    })