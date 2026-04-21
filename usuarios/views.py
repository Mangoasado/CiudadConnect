from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import FormularioLogin, FormularioRegistro, FormularioPerfil


def vista_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = FormularioLogin(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido, {user.nombre_completo}!')
                return redirect('dashboard')
        else:
            messages.error(request, 'El correo o la contraseña son incorrectos.')
    else:
        form = FormularioLogin(request)

    return render(request, 'usuarios/login.html', {'form': form})


def vista_registro(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = FormularioRegistro(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Cuenta creada correctamente! Bienvenido a CiudadConnect.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Por favor verifica los datos del formulario e intenta de nuevo.')
    else:
        form = FormularioRegistro()

    return render(request, 'usuarios/registro.html', {'form': form})


def vista_logout(request):
    logout(request)
    messages.success(request, '¡Sesión cerrada correctamente! Hasta pronto.')
    return redirect('login')


@login_required
def dashboard(request):
    return render(request, 'base/dashboard.html')


@login_required
def vista_perfil(request):
    if request.method == 'POST':
        form = FormularioPerfil(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('perfil')
        else:
            messages.error(request, 'Por favor corrige los errores.')
    else:
        form = FormularioPerfil(instance=request.user)

    # Estadísticas del usuario
    if request.user.es_administrador:
        mis_reportes = Reporte.objects.all()
    else:
        mis_reportes = request.user.reportes.all()
    contexto = {
        'form': form,
        'total_reportes': mis_reportes.count(),
        'pendientes': mis_reportes.filter(estado='pendiente').count(),
        'en_proceso': mis_reportes.filter(estado='en_proceso').count(),
        'resueltos': mis_reportes.filter(estado='resuelto').count(),
    }
    return render(request, 'usuarios/perfil.html', contexto)


@login_required
def cambiar_password(request):
    from django.contrib.auth import update_session_auth_hash
    from django.contrib.auth.forms import PasswordChangeForm

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Contraseña actualizada correctamente.')
            return redirect('perfil')
        else:
            messages.error(request, 'Por favor corrige los errores.')
    else:
        form = PasswordChangeForm(request.user)

    # Aplicar estilos Bootstrap al formulario
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'

    return render(request, 'usuarios/cambiar_password.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from reportes.models import Reporte
from .forms import FormularioLogin, FormularioRegistro, FormularioPerfil


@login_required
def dashboard(request):
    # Si es administrador ve todos los reportes, si no solo los suyos
    if request.user.es_administrador:
        reportes = Reporte.objects.all()
    else:
        reportes = Reporte.objects.filter(usuario=request.user)

    total = reportes.count()
    pendientes = reportes.filter(estado='pendiente').count()
    en_proceso = reportes.filter(estado='en_proceso').count()
    resueltos = reportes.filter(estado='resuelto').count()
    ultimos_reportes = reportes.order_by('-fecha_reporte')[:5]

    contexto = {
        'total': total,
        'pendientes': pendientes,
        'en_proceso': en_proceso,
        'resueltos': resueltos,
        'ultimos_reportes': ultimos_reportes,
    }
    return render(request, 'base/dashboard.html', contexto)