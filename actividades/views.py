from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ActividadForm
from .models import Actividad, EvidenciaActividad


@login_required
@permission_required('actividades.view_actividad', raise_exception=True)
def lista_actividades(request):
	query = request.GET.get('q', '').strip()
	actividades = Actividad.objects.select_related('categoria').prefetch_related('evidencias').order_by('-fecha_registro')
	if query:
		actividades = actividades.filter(
			Q(codigo_evidencia__icontains=query)
			| Q(titulo__icontains=query)
			| Q(descripcion__icontains=query)
			| Q(categoria__nombre__icontains=query)
		)
	return render(request, 'actividades/lista.html', {
		'actividades': actividades,
		'query': query,
	})


@permission_required('actividades.add_actividad', raise_exception=True)
def crear_actividad(request):
	form = ActividadForm(request.POST or None, request.FILES or None)
	if request.method == 'POST' and form.is_valid():
		actividad = form.save()
		for imagen in request.FILES.getlist('imagenes'):
			EvidenciaActividad.objects.create(actividad=actividad, imagen=imagen)
		return redirect('actividades:lista')
	return render(request, 'crud/formulario.html', {
		'form': form,
		'titulo': 'Agregar actividad',
		'texto_boton': 'Guardar actividad',
		'url_cancelar': 'actividades:lista',
	})


@permission_required('actividades.change_actividad', raise_exception=True)
def editar_actividad(request, pk):
	actividad = get_object_or_404(Actividad, pk=pk)
	form = ActividadForm(request.POST or None, request.FILES or None, instance=actividad)
	if request.method == 'POST' and form.is_valid():
		actividad = form.save()
		for imagen in request.FILES.getlist('imagenes'):
			EvidenciaActividad.objects.create(actividad=actividad, imagen=imagen)
		return redirect('actividades:lista')
	return render(request, 'crud/formulario.html', {
		'form': form,
		'titulo': 'Modificar actividad',
		'texto_boton': 'Guardar cambios',
		'url_cancelar': 'actividades:lista',
	})


@permission_required('actividades.delete_actividad', raise_exception=True)
def eliminar_actividad(request, pk):
	actividad = get_object_or_404(Actividad, pk=pk)
	if request.method == 'POST':
		actividad.delete()
		return redirect('actividades:lista')
	return render(request, 'crud/confirmar_eliminacion.html', {
		'objeto': actividad,
		'titulo': 'Eliminar actividad',
		'url_cancelar': 'actividades:lista',
	})
