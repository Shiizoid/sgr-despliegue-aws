from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from actividades.models import Actividad
from servicios.models import ServicioMunicipal, SolicitudServicio
from .forms import UsuarioCreationForm, UsuarioUpdateForm
from .roles import ROLE_MODELS


@login_required
def dashboard(request):
    profile = 'Administrador' if request.user.is_superuser else next(
        (name for name in ROLE_MODELS if request.user.groups.filter(name=name).exists()),
        None,
    )
    if profile is None:
        raise PermissionDenied('Tu cuenta todavía no tiene un perfil asignado.')

    solicitudes = SolicitudServicio.objects.all()
    if profile == 'Administrativo':
        solicitudes = solicitudes.filter(solicitante=request.user)

    context = {
        'perfil': profile,
        'total_actividades': Actividad.objects.count() if request.user.has_perm('actividades.view_actividad') else None,
        'total_servicios': ServicioMunicipal.objects.count() if request.user.has_perm('servicios.view_serviciomunicipal') else None,
        'total_solicitudes': solicitudes.count() if request.user.has_perm('servicios.view_solicitudservicio') else None,
        'total_usuarios': get_user_model().objects.count() if profile == 'Administrador' else None,
        'ultimas_solicitudes': solicitudes.select_related('servicio').order_by('-fecha_solicitud')[:5],
    }
    return render(request, 'dashboard/index.html', context)


@login_required
@permission_required('auth.view_user', raise_exception=True)
def lista_usuarios(request):
    usuarios = get_user_model().objects.prefetch_related('groups').order_by('username')
    return render(request, 'cuentas/usuarios.html', {'usuarios': usuarios})


@login_required
@permission_required('auth.add_user', raise_exception=True)
def crear_usuario(request):
    form = UsuarioCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'La cuenta se creó con el perfil seleccionado.')
        return redirect('cuentas:usuarios')
    return render(request, 'crud/formulario.html', {
        'form': form,
        'titulo': 'Crear usuario',
        'texto_boton': 'Crear usuario',
        'url_cancelar': 'cuentas:usuarios',
    })


@login_required
@permission_required('auth.change_user', raise_exception=True)
def editar_usuario(request, pk):
    usuario = get_object_or_404(get_user_model(), pk=pk)
    form = UsuarioUpdateForm(request.POST or None, instance=usuario)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Los datos y el perfil del usuario se actualizaron.')
        return redirect('cuentas:usuarios')
    return render(request, 'crud/formulario.html', {
        'form': form,
        'titulo': f'Editar usuario: {usuario.username}',
        'texto_boton': 'Guardar cambios',
        'url_cancelar': 'cuentas:usuarios',
    })
