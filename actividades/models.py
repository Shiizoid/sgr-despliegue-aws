from django.db import models


class Categoria(models.Model):
	nombre = models.CharField(max_length=100)
	descripcion = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.nombre


class Actividad(models.Model):
	codigo_evidencia = models.CharField(max_length=50, unique=True)
	titulo = models.CharField(max_length=150)
	descripcion = models.TextField()
	fecha_registro = models.DateTimeField(auto_now_add=True)
	categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='actividades')

	def __str__(self):
		return f"{self.codigo_evidencia} - {self.titulo}"


class EvidenciaActividad(models.Model):
	actividad = models.ForeignKey(
		Actividad,
		on_delete=models.CASCADE,
		related_name='evidencias',
	)
	imagen = models.ImageField(upload_to='actividades/evidencias/%Y/%m/')
	descripcion = models.CharField(max_length=160, blank=True)
	fecha_subida = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'Evidencia de {self.actividad.titulo}'
