from django.urls import path
from . import views

app_name = 'servicios'

urlpatterns = [
    path('', views.lista_servicios, name='lista'),
    path('nuevo/', views.crear_servicio, name='crear'),
    path('<int:pk>/editar/', views.editar_servicio, name='editar'),
    path('<int:pk>/eliminar/', views.eliminar_servicio, name='eliminar'),
    path('solicitudes/', views.lista_solicitudes, name='solicitudes'),
    path('solicitudes/nueva/', views.crear_solicitud, name='solicitud_crear'),
    path('solicitudes/<int:pk>/estado/', views.cambiar_estado_solicitud, name='solicitud_estado'),
]