from django.db import models


class ServicioMunicipal(models.Model):
	nombre_servicio = models.CharField(max_length=120)
	responsable = models.CharField(max_length=100)
	activo = models.BooleanField(default=True)

	def __str__(self):
		return self.nombre_servicio
