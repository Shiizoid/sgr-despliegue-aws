from django.urls import path
from . import views

app_name = 'actividades'

urlpatterns = [
    path('', views.lista_actividades, name='lista'),
    path('nueva/', views.crear_actividad, name='crear'),
    path('<int:pk>/editar/', views.editar_actividad, name='editar'),
    path('<int:pk>/eliminar/', views.eliminar_actividad, name='eliminar'),
]