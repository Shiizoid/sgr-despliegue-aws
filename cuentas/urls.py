from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

app_name = 'cuentas'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='cuentas/login.html',
        redirect_authenticated_user=True,
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='cuentas/password_reset_form.html',
        email_template_name='cuentas/password_reset_email.html',
        subject_template_name='cuentas/password_reset_subject.txt',
        success_url=reverse_lazy('cuentas:password_reset_done'),
    ), name='password_reset'),
    path('password-reset/enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='cuentas/password_reset_done.html',
    ), name='password_reset_done'),
    path('password-reset/confirmar/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='cuentas/password_reset_confirm.html',
        success_url=reverse_lazy('cuentas:password_reset_complete'),
    ), name='password_reset_confirm'),
    path('password-reset/completado/', auth_views.PasswordResetCompleteView.as_view(
        template_name='cuentas/password_reset_complete.html',
    ), name='password_reset_complete'),
    path('panel/', views.dashboard, name='dashboard'),
    path('usuarios/', views.lista_usuarios, name='usuarios'),
    path('usuarios/nuevo/', views.crear_usuario, name='usuario_crear'),
    path('usuarios/<int:pk>/editar/', views.editar_usuario, name='usuario_editar'),
]
