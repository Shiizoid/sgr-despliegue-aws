from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ServicioMunicipalForm, SolicitudEstadoForm, SolicitudServicioForm
from .models import ServicioMunicipal, SolicitudServicio


def lista_servicios(request):
	query = request.GET.get('q', '').strip()
	servicios = ServicioMunicipal.objects.prefetch_related('evidencias').order_by('nombre_servicio')
	if query:
		servicios = servicios.filter(
			Q(nombre_servicio__icontains=query)
			| Q(responsable__icontains=query)
		)
	return render(request, 'servicios/lista.html', {
		'servicios': servicios,
		'query': query,
	})


@permission_required('servicios.add_serviciomunicipal', raise_exception=True)
def crear_servicio(request):
	form = ServicioMunicipalForm(request.POST or None, request.FILES or None)
	if request.method == 'POST' and form.is_valid():
		servicio = form.save()
		for imagen in request.FILES.getlist('imagenes'):
			EvidenciaServicio.objects.create(servicio=servicio, imagen=imagen)
		return redirect('servicios:lista')
	return render(request, 'crud/formulario.html', {
		'form': form,
		'titulo': 'Agregar servicio municipal',
		'texto_boton': 'Guardar servicio',
		'url_cancelar': 'servicios:lista',
	})


@permission_required('servicios.change_serviciomunicipal', raise_exception=True)
def editar_servicio(request, pk):
	servicio = get_object_or_404(ServicioMunicipal, pk=pk)
	form = ServicioMunicipalForm(request.POST or None, request.FILES or None, instance=servicio)
	if request.method == 'POST' and form.is_valid():
		servicio = form.save()
		for imagen in request.FILES.getlist('imagenes'):
			EvidenciaServicio.objects.create(servicio=servicio, imagen=imagen)
		return redirect('servicios:lista')
	return render(request, 'crud/formulario.html', {
		'form': form,
		'titulo': 'Modificar servicio municipal',
		'texto_boton': 'Guardar cambios',
		'url_cancelar': 'servicios:lista',
	})


@permission_required('servicios.delete_serviciomunicipal', raise_exception=True)
def eliminar_servicio(request, pk):
	servicio = get_object_or_404(ServicioMunicipal, pk=pk)
	if request.method == 'POST':
		servicio.delete()
		return redirect('servicios:lista')
	return render(request, 'crud/confirmar_eliminacion.html', {
		'objeto': servicio,
		'titulo': 'Eliminar servicio municipal',
		'url_cancelar': 'servicios:lista',
	})


@login_required
@permission_required('servicios.view_solicitudservicio', raise_exception=True)
def lista_solicitudes(request):
	solicitudes = SolicitudServicio.objects.select_related('servicio', 'solicitante')
	if not request.user.has_perm('servicios.change_solicitudservicio'):
		solicitudes = solicitudes.filter(solicitante=request.user)
	query = request.GET.get('q', '').strip()
	if query:
		solicitudes = solicitudes.filter(
			Q(servicio__nombre_servicio__icontains=query)
			| Q(solicitante__username__icontains=query)
			| Q(descripcion__icontains=query)
		)
	return render(request, 'servicios/solicitudes.html', {
		'solicitudes': solicitudes,
		'query': query,
	})


@login_required
@permission_required('servicios.add_solicitudservicio', raise_exception=True)
def crear_solicitud(request):
	form = SolicitudServicioForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		solicitud = form.save(commit=False)
		solicitud.solicitante = request.user
		solicitud.save()
		messages.success(request, 'La solicitud se registró correctamente.')
		return redirect('servicios:solicitudes')
	return render(request, 'crud/formulario.html', {
		'form': form,
		'titulo': 'Registrar solicitud de servicio',
		'texto_boton': 'Enviar solicitud',
		'url_cancelar': 'servicios:solicitudes',
	})


@login_required
@permission_required('servicios.change_solicitudservicio', raise_exception=True)
def cambiar_estado_solicitud(request, pk):
	solicitud = get_object_or_404(SolicitudServicio, pk=pk)
	form = SolicitudEstadoForm(request.POST or None, instance=solicitud)
	if request.method == 'POST' and form.is_valid():
		form.save()
		messages.success(request, f'El estado de la solicitud #{solicitud.pk} se actualizó.')
		return redirect('servicios:solicitudes')
	return render(request, 'crud/formulario.html', {
		'form': form,
		'titulo': f'Actualizar solicitud #{solicitud.pk}',
		'texto_boton': 'Guardar estado',
		'url_cancelar': 'servicios:solicitudes',
	})
