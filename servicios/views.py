from django.shortcuts import render
from .models import ServicioMunicipal


def lista_servicios(request):
	servicios = ServicioMunicipal.objects.order_by('nombre_servicio')
	return render(request, 'servicios/lista.html', {'servicios': servicios})
