from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from urllib.parse import urlsplit

from servicios.models import ServicioMunicipal


class CuentasAccessTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.admin = user_model.objects.create_user(
            username='administrador',
            password='ClaveSegura123!',
            email='admin@example.com',
        )
        cls.supervisor = user_model.objects.create_user(
            username='supervisor',
            password='ClaveSegura123!',
            email='supervisor@example.com',
        )
        cls.administrativo = user_model.objects.create_user(
            username='administrativo',
            password='ClaveSegura123!',
            email='administrativo@example.com',
        )
        cls.superadmin = user_model.objects.create_superuser(
            username='superadmin',
            password='ClaveSegura123!',
            email='superadmin@example.com',
        )
        cls._assign_permissions(cls.admin, 'Administrador', (
            ('view_user', 'auth'),
            ('add_user', 'auth'),
            ('view_actividad', 'actividades'),
            ('add_actividad', 'actividades'),
            ('change_actividad', 'actividades'),
            ('delete_actividad', 'actividades'),
        ))
        cls._assign_permissions(cls.supervisor, 'Supervisor', (
            ('view_actividad', 'actividades'),
            ('change_actividad', 'actividades'),
        ))
        cls._assign_permissions(cls.administrativo, 'Administrativo', (
            ('view_actividad', 'actividades'),
            ('view_serviciomunicipal', 'servicios'),
            ('view_solicitudservicio', 'servicios'),
            ('add_solicitudservicio', 'servicios'),
        ))
        cls.superadmin.groups.set((Group.objects.get(name='Administrativo'),))
        cls.servicio = ServicioMunicipal.objects.create(
            nombre_servicio='Atención municipal',
            responsable='Equipo de atención',
            activo=True,
        )

    @staticmethod
    def _assign_permissions(user, group_name, permissions):
        group, _ = Group.objects.get_or_create(name=group_name)
        for codename, app_label in permissions:
            permission = Permission.objects.get(
                codename=codename,
                content_type__app_label=app_label,
            )
            group.permissions.add(permission)
        user.groups.add(group)

    def test_dashboard_redirects_to_login_and_login_opens_panel(self):
        response = self.client.get(reverse('cuentas:dashboard'))
        self.assertRedirects(response, f"{reverse('cuentas:login')}?next={reverse('cuentas:dashboard')}")

        self.assertTrue(self.client.login(username='administrativo', password='ClaveSegura123!'))
        response = self.client.get(reverse('cuentas:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Acceso Administrativo')

    def test_permissions_are_enforced_by_views_not_only_navigation(self):
        self.client.force_login(self.administrativo)
        self.assertEqual(self.client.get(reverse('actividades:crear')).status_code, 403)

        self.client.force_login(self.supervisor)
        self.assertEqual(self.client.get(reverse('actividades:editar', args=(1,))).status_code, 404)
        self.assertEqual(self.client.get(reverse('cuentas:usuarios')).status_code, 403)

        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(reverse('cuentas:usuarios')).status_code, 200)

    def test_builtin_admin_site_is_not_exposed(self):
        self.assertEqual(self.client.get('/admin/').status_code, 404)

    def test_public_portal_and_maintainer_lists_render(self):
        for path in ('/', reverse('actividades:lista'), reverse('servicios:lista')):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)

    def test_default_roles_have_different_permission_levels(self):
        admin = Group.objects.get(name='Administrador')
        supervisor = Group.objects.get(name='Supervisor')
        administrativo = Group.objects.get(name='Administrativo')

        self.assertTrue(admin.permissions.filter(codename='view_user').exists())
        self.assertTrue(supervisor.permissions.filter(codename='add_serviciomunicipal').exists())
        self.assertFalse(supervisor.permissions.filter(codename='delete_serviciomunicipal').exists())
        self.assertTrue(administrativo.permissions.filter(codename='add_solicitudservicio').exists())
        self.assertFalse(administrativo.permissions.filter(codename='change_serviciomunicipal').exists())

    def test_superuser_keeps_full_access_and_is_labeled_beside_assigned_role(self):
        self.client.force_login(self.superadmin)
        response = self.client.get(reverse('cuentas:usuarios'))
        self.assertContains(response, 'Administrativo')
        self.assertContains(response, 'SUPERADMIN')

        response = self.client.get(reverse('cuentas:dashboard'))
        self.assertContains(response, 'Acceso Administrador · SUPERADMIN')
        self.assertContains(response, 'conserva acceso total como superusuario')
        self.assertTrue(self.superadmin.has_perm('servicios.delete_serviciomunicipal'))

    def test_administrator_can_create_a_user_with_a_role(self):
        self.client.force_login(self.admin)
        supervisor_group = Group.objects.get(name='Supervisor')
        response = self.client.post(reverse('cuentas:usuario_crear'), {
            'username': 'nuevo-supervisor',
            'first_name': 'Nuevo',
            'last_name': 'Supervisor',
            'email': 'nuevo.supervisor@example.com',
            'password1': 'UnaClaveFuerte!8472',
            'password2': 'UnaClaveFuerte!8472',
            'rol': supervisor_group.pk,
        })
        self.assertRedirects(response, reverse('cuentas:usuarios'))
        created = get_user_model().objects.get(username='nuevo-supervisor')
        self.assertEqual(created.email, 'nuevo.supervisor@example.com')
        self.assertTrue(created.groups.filter(name='Supervisor').exists())

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_password_reset_email_link_changes_password(self):
        response = self.client.post(
            reverse('cuentas:password_reset'),
            {'email': self.administrativo.email},
        )
        self.assertRedirects(response, reverse('cuentas:password_reset_done'))
        self.assertEqual(len(mail.outbox), 1)

        response = self.client.get(reverse('cuentas:password_reset_done'))
        self.assertEqual(response.status_code, 200)
        reset_url = next(
            line for line in mail.outbox[0].body.splitlines()
            if line.startswith(('http://', 'https://'))
        )
        response = self.client.get(urlsplit(reset_url).path, follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(response.request['PATH_INFO'], {
            'new_password1': 'NuevaClaveSegura456!',
            'new_password2': 'NuevaClaveSegura456!',
        })
        self.assertRedirects(response, reverse('cuentas:password_reset_complete'))
        self.administrativo.refresh_from_db()
        self.assertTrue(self.administrativo.check_password('NuevaClaveSegura456!'))
