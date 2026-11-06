from django.contrib import admin

from .models import EvidenciaServicio, ServicioMunicipal, SolicitudServicio


@admin.register(ServicioMunicipal)
class ServicioMunicipalAdmin(admin.ModelAdmin):
    list_display = ('nombre_servicio', 'responsable', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre_servicio', 'responsable')


@admin.register(EvidenciaServicio)
class EvidenciaServicioAdmin(admin.ModelAdmin):
    list_display = ('servicio', 'descripcion', 'fecha_subida')
    search_fields = ('servicio__nombre_servicio', 'descripcion')
    readonly_fields = ('fecha_subida',)


@admin.register(SolicitudServicio)
class SolicitudServicioAdmin(admin.ModelAdmin):
    list_display = ('id', 'servicio', 'solicitante', 'tipo_solicitud', 'estado', 'fecha_solicitud')
    list_filter = ('tipo_solicitud', 'estado', 'fecha_solicitud')
    search_fields = ('servicio__nombre_servicio', 'solicitante__username', 'descripcion')
    readonly_fields = ('solicitante', 'servicio', 'tipo_solicitud', 'telefono', 'descripcion', 'fecha_solicitud')
