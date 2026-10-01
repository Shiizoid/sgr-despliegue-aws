from django.contrib import admin
from .models import ServicioMunicipal


@admin.register(ServicioMunicipal)
class ServicioMunicipalAdmin(admin.ModelAdmin):
	list_display = ('id', 'nombre_servicio', 'responsable', 'activo')
	search_fields = ('nombre_servicio', 'responsable')
	list_filter = ('activo',)
