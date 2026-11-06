from io import BytesIO
from tempfile import TemporaryDirectory

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from urllib.parse import urlsplit

from actividades.models import Actividad, Categoria, EvidenciaActividad
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
        user_without_permissions = get_user_model().objects.create_user(
            username='sin-permisos-listados',
            password='ClaveSegura123!',
        )
        self.client.force_login(user_without_permissions)
        self.assertEqual(self.client.get(reverse('actividades:lista')).status_code, 403)
        self.assertEqual(self.client.get(reverse('servicios:lista')).status_code, 403)

        self.client.force_login(self.administrativo)
        self.assertEqual(self.client.get(reverse('actividades:crear')).status_code, 403)

        self.client.force_login(self.supervisor)
        self.assertEqual(self.client.get(reverse('actividades:editar', args=(1,))).status_code, 404)
        self.assertEqual(self.client.get(reverse('cuentas:usuarios')).status_code, 403)

        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(reverse('cuentas:usuarios')).status_code, 200)

    def test_builtin_admin_site_requires_authentication_and_superuser_access(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(f"{reverse('admin:login')}?next="))

        self.client.force_login(self.administrativo)
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(f"{reverse('admin:login')}?next="))

        self.client.force_login(self.superadmin)
        self.assertEqual(self.client.get('/admin/').status_code, 200)

    def test_public_portal_is_available_but_data_lists_require_login(self):
        self.assertEqual(self.client.get('/').status_code, 200)

        for path in (reverse('actividades:lista'), reverse('servicios:lista')):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertRedirects(
                    response,
                    f"{reverse('cuentas:login')}?next={path}",
                )

        self.client.force_login(self.administrativo)
        self.assertEqual(self.client.get(reverse('actividades:lista')).status_code, 200)
        self.assertEqual(self.client.get(reverse('servicios:lista')).status_code, 200)

    def test_media_requires_authentication_and_view_permission(self):
        image_buffer = BytesIO()
        Image.new('RGB', (8, 8), color='teal').save(image_buffer, format='PNG')
        image = SimpleUploadedFile(
            'evidence.png',
            image_buffer.getvalue(),
            content_type='image/png',
        )
        category = Categoria.objects.create(nombre='Privada', descripcion='')
        activity = Actividad.objects.create(
            codigo_evidencia='PRIV-001',
            titulo='Actividad privada',
            descripcion='Prueba de acceso a evidencias.',
            categoria=category,
        )

        with TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                evidence = EvidenciaActividad.objects.create(actividad=activity, imagen=image)
                media_path = evidence.imagen.name
                media_url = reverse('authenticated_media', kwargs={'path': media_path})

                response = self.client.get(media_url)
                self.assertRedirects(
                    response,
                    f"{reverse('cuentas:login')}?next={media_url}",
                )

                user_model = get_user_model()
                no_permission_user = user_model.objects.create_user(
                    username='sin-permisos',
                    password='ClaveSegura123!',
                )
                self.client.force_login(no_permission_user)
                self.assertEqual(self.client.get(media_url).status_code, 403)

                self.client.force_login(self.supervisor)
                response = self.client.get(media_url)
                try:
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(response['Content-Type'], 'image/png')
                finally:
                    response.close()

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
        self.assertTrue(hasattr(created, 'perfil'))

    def test_duplicate_email_or_username_is_rejected_without_changing_existing_account(self):
        self.client.force_login(self.admin)
        supervisor_group = Group.objects.get(name='Supervisor')
        original_password = 'ClaveSegura123!'
        original_count = get_user_model().objects.count()

        duplicate_email_response = self.client.post(reverse('cuentas:usuario_crear'), {
            'username': 'otro-usuario',
            'first_name': 'Intento',
            'last_name': 'Duplicado',
            'email': self.administrativo.email.upper(),
            'password1': 'UnaClaveFuerte!8472',
            'password2': 'UnaClaveFuerte!8472',
            'rol': supervisor_group.pk,
        })
        self.assertEqual(duplicate_email_response.status_code, 200)
        self.assertContains(duplicate_email_response, 'Esta cuenta ya está creada: el correo electrónico ya está en uso.')

        duplicate_username_response = self.client.post(reverse('cuentas:usuario_crear'), {
            'username': self.administrativo.username,
            'first_name': 'Intento',
            'last_name': 'Duplicado',
            'email': 'otro.correo@example.com',
            'password1': 'UnaClaveFuerte!8472',
            'password2': 'UnaClaveFuerte!8472',
            'rol': supervisor_group.pk,
        })
        self.assertEqual(duplicate_username_response.status_code, 200)
        self.assertContains(duplicate_username_response, 'Este nombre de usuario ya está registrado. Elige otro.')

        self.administrativo.refresh_from_db()
        self.assertEqual(get_user_model().objects.count(), original_count)
        self.assertEqual(self.administrativo.email, 'administrativo@example.com')
        self.assertTrue(self.administrativo.check_password(original_password))

    def test_user_can_update_own_name_last_name_and_profile_image(self):
        image_buffer = BytesIO()
        Image.new('RGB', (8, 8), color='teal').save(image_buffer, format='PNG')
        image = SimpleUploadedFile(
            'foto.png',
            image_buffer.getvalue(),
            content_type='image/png',
        )
        self.client.force_login(self.administrativo)
        with TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                response = self.client.post(reverse('cuentas:perfil'), {
                    'first_name': 'Mauricio',
                    'last_name': 'Muñiz',
                    'imagen': image,
                })
                self.assertRedirects(response, reverse('cuentas:perfil'))
                self.administrativo.refresh_from_db()
                self.assertEqual(self.administrativo.first_name, 'Mauricio')
                self.assertEqual(self.administrativo.last_name, 'Muñiz')
                self.assertTrue(self.administrativo.perfil.imagen)
                response = self.client.get(reverse('cuentas:perfil'))
                self.assertContains(response, 'Mauricio Muñiz')
                self.assertContains(response, self.administrativo.perfil.imagen.url)
                self.assertContains(response, 'Editar perfil de Mauricio Muñiz')

                response = self.client.post(reverse('cuentas:perfil'), {
                    'first_name': 'Mauricio',
                    'last_name': 'Muñiz',
                    'imagen-clear': 'on',
                })
                self.assertRedirects(response, reverse('cuentas:perfil'))
                self.administrativo.perfil.refresh_from_db()
                self.assertFalse(self.administrativo.perfil.imagen)

                self.client.force_login(self.administrativo)
                response = self.client.post(reverse('cuentas:perfil'), {
                    'first_name': 'Mauricio',
                    'last_name': 'Muñiz',
                    'imagen': SimpleUploadedFile(
                        'foto-lista.png',
                        image_buffer.getvalue(),
                        content_type='image/png',
                    ),
                })
                self.assertRedirects(response, reverse('cuentas:perfil'))
                self.administrativo.perfil.refresh_from_db()
                self.client.force_login(self.admin)
                response = self.client.get(reverse('cuentas:usuarios'))
                self.assertContains(response, 'Mauricio Muñiz')
                self.assertContains(response, self.administrativo.perfil.imagen.url)

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
