from django.urls import path
from . import views

app_name = 'servicios'

urlpatterns = [
    path('', views.lista_servicios, name='lista'),
    path('nuevo/', views.crear_servicio, name='crear'),
    path('<int:pk>/editar/', views.editar_servicio, name='editar'),
    path('<int:pk>/eliminar/', views.eliminar_servicio, name='eliminar'),
]