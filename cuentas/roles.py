from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver


ROLE_MODELS = {
    'Administrador': {
        'actividades': ('categoria', 'actividad', 'evidenciaactividad'),
        'servicios': ('serviciomunicipal', 'evidenciaservicio', 'solicitudservicio'),
        'auth': ('user',),
    },
    'Supervisor': {
        'actividades': ('categoria', 'actividad', 'evidenciaactividad'),
        'servicios': ('serviciomunicipal', 'evidenciaservicio', 'solicitudservicio'),
    },
    'Administrativo': {
        'actividades': ('categoria', 'actividad', 'evidenciaactividad'),
        'servicios': ('serviciomunicipal', 'evidenciaservicio', 'solicitudservicio'),
    },
}

ROLE_ACTIONS = {
    'Administrador': ('view', 'add', 'change', 'delete'),
    'Supervisor': ('view', 'add', 'change'),
    'Administrativo': ('view',),
}


@receiver(post_migrate, dispatch_uid='cuentas.create_default_roles')
def create_default_roles(sender, **kwargs):
    for role, app_models in ROLE_MODELS.items():
        group, _ = Group.objects.get_or_create(name=role)
        permission_codenames = [
            f'{action}_{model}'
            for app_label, model_names in app_models.items()
            for model in model_names
            for action in ROLE_ACTIONS[role]
        ]
        if role == 'Administrador':
            permission_codenames.extend(('add_user', 'change_user', 'view_user'))
        if role == 'Administrativo':
            permission_codenames.append('add_solicitudservicio')
        permissions = Permission.objects.filter(
            content_type__app_label__in=app_models,
            codename__in=permission_codenames,
        )
        group.permissions.add(*permissions)
