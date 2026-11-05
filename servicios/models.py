from django.conf import settings
from django.core.validators import RegexValidator
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


class SolicitudServicio(models.Model):
	class Estado(models.TextChoices):
		PENDIENTE = 'pendiente', 'Pendiente'
		EN_REVISION = 'en_revision', 'En revisión'
		RESUELTA = 'resuelta', 'Resuelta'
		RECHAZADA = 'rechazada', 'Rechazada'

	solicitante = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.PROTECT,
		related_name='solicitudes_servicio',
	)
	servicio = models.ForeignKey(
		ServicioMunicipal,
		on_delete=models.PROTECT,
		related_name='solicitudes',
	)
	telefono = models.CharField(
		max_length=20,
		validators=[RegexValidator(r'^[0-9+()\-\s]{6,20}$', 'Ingresa un teléfono válido.')],
	)
	descripcion = models.TextField(max_length=1000)
	estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)
	fecha_solicitud = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-fecha_solicitud',)

	def __str__(self):
		return f'Solicitud #{self.pk} - {self.servicio.nombre_servicio}'
