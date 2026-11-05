from .roles import ROLE_MODELS


def user_role(request):
    if not request.user.is_authenticated:
        return {'role_label': '', 'can_manage_users': False, 'is_superadmin': False}

    role = next(
        (name for name in ROLE_MODELS if request.user.groups.filter(name=name).exists()),
        'Administrador' if request.user.is_superuser else 'Sin perfil asignado',
    )
    return {
        'role_label': role,
        'can_manage_users': request.user.is_superuser or role == 'Administrador',
        'is_superadmin': request.user.is_superuser,
    }
