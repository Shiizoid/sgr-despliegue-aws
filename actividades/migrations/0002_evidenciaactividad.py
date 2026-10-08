import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

	dependencies = [
		('actividades', '0001_initial'),
	]

	operations = [
		migrations.CreateModel(
			name='EvidenciaActividad',
			fields=[
				('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('imagen', models.ImageField(upload_to='actividades/evidencias/%Y/%m/')),
				('descripcion', models.CharField(blank=True, max_length=160)),
				('fecha_subida', models.DateTimeField(auto_now_add=True)),
				('actividad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evidencias', to='actividades.actividad')),
			],
		),
	]