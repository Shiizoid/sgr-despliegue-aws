from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ServicioMunicipalForm
from .models import ServicioMunicipal


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


@login_required(login_url='/admin/login/')
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


@login_required(login_url='/admin/login/')
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


@login_required(login_url='/admin/login/')
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
