from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ActividadForm
from .models import Actividad


def lista_actividades(request):
	query = request.GET.get('q', '').strip()
	actividades = Actividad.objects.select_related('categoria').order_by('-fecha_registro')
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


@login_required(login_url='/admin/login/')
def crear_actividad(request):
	form = ActividadForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		form.save()
		return redirect('actividades:lista')
	return render(request, 'crud/formulario.html', {
		'form': form,
		'titulo': 'Agregar actividad',
		'texto_boton': 'Guardar actividad',
		'url_cancelar': 'actividades:lista',
	})


@login_required(login_url='/admin/login/')
def editar_actividad(request, pk):
	actividad = get_object_or_404(Actividad, pk=pk)
	form = ActividadForm(request.POST or None, instance=actividad)
	if request.method == 'POST' and form.is_valid():
		form.save()
		return redirect('actividades:lista')
	return render(request, 'crud/formulario.html', {
		'form': form,
		'titulo': 'Modificar actividad',
		'texto_boton': 'Guardar cambios',
		'url_cancelar': 'actividades:lista',
	})


@login_required(login_url='/admin/login/')
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
