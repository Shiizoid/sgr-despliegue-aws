from django.contrib import admin
from .models import Categoria, Actividad


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
	list_display = ('id', 'nombre')
	search_fields = ('nombre',)


@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
	list_display = ('codigo_evidencia', 'titulo', 'categoria', 'fecha_registro')
	list_filter = ('categoria', 'fecha_registro')
	search_fields = ('codigo_evidencia', 'titulo', 'descripcion')
