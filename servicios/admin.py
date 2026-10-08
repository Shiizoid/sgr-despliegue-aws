from django.contrib import admin
from django.utils.html import format_html
from .models import EvidenciaServicio, ServicioMunicipal


class EvidenciaServicioInline(admin.TabularInline):
	model = EvidenciaServicio
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


@admin.register(ServicioMunicipal)
class ServicioMunicipalAdmin(admin.ModelAdmin):
	list_display = ('id', 'nombre_servicio', 'responsable', 'activo')
	search_fields = ('nombre_servicio', 'responsable')
	list_filter = ('activo',)
	inlines = (EvidenciaServicioInline,)
