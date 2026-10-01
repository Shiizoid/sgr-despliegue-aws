from django.urls import path
from . import views

app_name = 'actividades'

urlpatterns = [
    path('', views.lista_actividades, name='lista'),
]