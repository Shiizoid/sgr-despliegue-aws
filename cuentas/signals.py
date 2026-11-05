from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import PerfilUsuario


@receiver(post_save, sender=get_user_model(), dispatch_uid='cuentas.ensure_user_profile')
def ensure_user_profile(sender, instance, **kwargs):
    PerfilUsuario.objects.get_or_create(usuario=instance)
