from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Categoria, Actividad, EvidenciaActividad


class EvidenciaActividadInline(admin.TabularInline):
	model = EvidenciaActividad
	extra = 1
	max_num = 6
	fields = ('imagen', 'descripcion', 'vista_previa', 'fecha_subida')
	readonly_fields = ('vista_previa', 'fecha_subida')

	@admin.display(description='Vista previa')
	def vista_previa(self, obj):
		if obj and obj.imagen:
			return format_html(
				'<img src="{}" alt="" style="max-height:90px;max-width:140px">',
				obj.imagen.url,
			)
		return 'Guarda la imagen para ver la vista previa.'


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
	list_display = ('id', 'nombre', 'editar_enlace')
	search_fields = ('nombre',)

	@admin.display(description='Acción')
	def editar_enlace(self, obj):
		url = reverse('admin:actividades_categoria_change', args=[obj.pk])
		return format_html('<a href="{}">Editar</a>', url)


@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
	list_display = ('codigo_evidencia', 'titulo', 'categoria', 'fecha_registro', 'editar_enlace')
	list_filter = ('categoria', 'fecha_registro')
	search_fields = ('codigo_evidencia', 'titulo', 'descripcion')
	inlines = (EvidenciaActividadInline,)

	@admin.display(description='Acción')
	def editar_enlace(self, obj):
		url = reverse('admin:actividades_actividad_change', args=[obj.pk])
		return format_html('<a href="{}">Editar</a>', url)
