from django.db import models


class ServicioMunicipal(models.Model):
	nombre_servicio = models.CharField(max_length=120)
	responsable = models.CharField(max_length=100)
	activo = models.BooleanField(default=True)

	def __str__(self):
		return self.nombre_servicio


class EvidenciaServicio(models.Model):
	servicio = models.ForeignKey(
		ServicioMunicipal,
		on_delete=models.CASCADE,
		related_name='evidencias',
	)
	imagen = models.ImageField(upload_to='servicios/evidencias/%Y/%m/')
	descripcion = models.CharField(max_length=160, blank=True)
	fecha_subida = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'Evidencia de {self.servicio.nombre_servicio}'
