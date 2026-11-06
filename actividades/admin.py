from django.contrib import admin

from .models import Actividad, Categoria, EvidenciaActividad


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)
    list_display = ('nombre',)


@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ('codigo_evidencia', 'titulo', 'categoria', 'fecha_registro')
    list_filter = ('categoria',)
    search_fields = ('codigo_evidencia', 'titulo', 'descripcion')
    readonly_fields = ('fecha_registro',)


@admin.register(EvidenciaActividad)
class EvidenciaActividadAdmin(admin.ModelAdmin):
    list_display = ('actividad', 'descripcion', 'fecha_subida')
    search_fields = ('actividad__titulo', 'descripcion')
    readonly_fields = ('fecha_subida',)
