from django.shortcuts import render
from .models import Actividad


def lista_actividades(request):
	actividades = Actividad.objects.select_related('categoria').order_by('-fecha_registro')
	return render(request, 'actividades/lista.html', {'actividades': actividades})
