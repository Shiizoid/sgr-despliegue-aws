from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from django.urls import reverse

from .models import ServicioMunicipal, SolicitudServicio


class SolicitudServicioTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.solicitante = user_model.objects.create_user(
            username='vecino',
            password='ClaveSegura123!',
            email='vecino@example.com',
        )
        cls.otro_solicitante = user_model.objects.create_user(
            username='otra-vecina',
            password='ClaveSegura123!',
            email='otra@example.com',
        )
        cls.supervisor = user_model.objects.create_user(
            username='supervisor-servicios',
            password='ClaveSegura123!',
            email='supervisor-servicios@example.com',
        )
        cls._assign_permissions(cls.solicitante, 'Administrativo', (
            'view_solicitudservicio',
            'add_solicitudservicio',
        ))
        cls._assign_permissions(cls.otro_solicitante, 'Administrativo', (
            'view_solicitudservicio',
            'add_solicitudservicio',
        ))
        cls._assign_permissions(cls.supervisor, 'Supervisor', (
            'view_solicitudservicio',
            'change_solicitudservicio',
        ))
        cls.servicio = ServicioMunicipal.objects.create(
            nombre_servicio='Permiso municipal',
            responsable='Dirección municipal',
            activo=True,
        )
        cls.solicitud = SolicitudServicio.objects.create(
            solicitante=cls.solicitante,
            servicio=cls.servicio,
            telefono='+56 9 1234 5678',
            descripcion='Necesito información para realizar el trámite.',
        )

    @staticmethod
    def _assign_permissions(user, group_name, codenames):
        group, _ = Group.objects.get_or_create(name=group_name)
        permissions = Permission.objects.filter(
            codename__in=codenames,
            content_type__app_label='servicios',
        )
        group.permissions.add(*permissions)
        user.groups.add(group)

    def test_request_is_saved_with_user_and_service_relationships(self):
        self.client.force_login(self.solicitante)
        response = self.client.post(reverse('servicios:solicitud_crear'), {
            'servicio': self.servicio.pk,
            'telefono': '+56 9 9999 8888',
            'descripcion': 'Solicito orientación sobre el servicio.',
        })
        self.assertRedirects(response, reverse('servicios:solicitudes'))
        solicitud = SolicitudServicio.objects.get(telefono='+56 9 9999 8888')
        self.assertEqual(solicitud.solicitante, self.solicitante)
        self.assertEqual(solicitud.servicio, self.servicio)
        self.assertEqual(solicitud.estado, SolicitudServicio.Estado.PENDIENTE)

    def test_users_only_see_their_own_requests_and_cannot_change_status(self):
        SolicitudServicio.objects.create(
            solicitante=self.otro_solicitante,
            servicio=self.servicio,
            telefono='+56 9 8765 4321',
            descripcion='Otra solicitud de prueba.',
        )
        self.client.force_login(self.otro_solicitante)
        response = self.client.get(reverse('servicios:solicitudes'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context['solicitudes'].values_list('solicitante_id', flat=True)),
            [self.otro_solicitante.pk],
        )
        self.assertEqual(
            self.client.post(
                reverse('servicios:solicitud_estado', args=(self.solicitud.pk,)),
                {'estado': SolicitudServicio.Estado.RESUELTA},
            ).status_code,
            403,
        )

    def test_supervisor_can_update_request_status(self):
        self.client.force_login(self.supervisor)
        response = self.client.post(
            reverse('servicios:solicitud_estado', args=(self.solicitud.pk,)),
            {'estado': SolicitudServicio.Estado.EN_REVISION},
        )
        self.assertRedirects(response, reverse('servicios:solicitudes'))
        self.solicitud.refresh_from_db()
        self.assertEqual(self.solicitud.estado, SolicitudServicio.Estado.EN_REVISION)
