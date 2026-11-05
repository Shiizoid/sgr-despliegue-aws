from django.conf import settings
from django.db import models


class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil',
    )
    imagen = models.ImageField(upload_to='perfiles/', blank=True)

    def __str__(self):
        return f'Perfil de {self.usuario.get_full_name() or self.usuario.username}'
