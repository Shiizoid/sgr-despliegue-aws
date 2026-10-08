import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

	dependencies = [
		('servicios', '0001_initial'),
	]

	operations = [
		migrations.CreateModel(
			name='EvidenciaServicio',
			fields=[
				('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('imagen', models.ImageField(upload_to='servicios/evidencias/%Y/%m/')),
				('descripcion', models.CharField(blank=True, max_length=160)),
				('fecha_subida', models.DateTimeField(auto_now_add=True)),
				('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evidencias', to='servicios.serviciomunicipal')),
			],
		),
	]