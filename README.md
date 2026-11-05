# SGR La Serena

Aplicación web Django para administrar actividades y servicios municipales.

## Requisitos

- Python 3.12.
- MySQL o MariaDB instalado y en ejecución.
- Git para clonar o publicar el proyecto.

## Configuración local

Desde la raíz del proyecto, crea y activa un entorno virtual en PowerShell:

```powershell
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Crea un archivo `.env` en la raíz. Usa valores locales y no lo publiques en GitHub:

```dotenv
SECRET_KEY=una-clave-secreta-local
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=sgr_db
DB_USER=root
DB_PASSWORD=tu_password_mysql
DB_HOST=127.0.0.1
DB_PORT=3306
```

Crea la base de datos `sgr_db` en MySQL/MariaDB y luego ejecuta:

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

La aplicación estará disponible en `http://127.0.0.1:8000/`. Inicia sesión en `http://127.0.0.1:8000/cuentas/login/`; el panel propio aparece en `http://127.0.0.1:8000/cuentas/panel/`. Django Admin no está expuesto.

## Aplicaciones

- `actividades`: categorías y actividades, relacionadas mediante clave foránea.
- `servicios`: servicios municipales.

El archivo `.env` y los entornos virtuales están excluidos mediante `.gitignore`.

## Evaluación Sumativa 3

La aplicación continúa el proyecto anterior e incorpora:

- Inicio y cierre de sesión desde páginas propias; `/admin/` no está habilitado.
- Perfiles `Administrador`, `Supervisor` y `Administrativo`, creados automáticamente al ejecutar las migraciones.
- Mantenedores de actividades y servicios con permisos por perfil; las operaciones se hacen con Django Templates.
- Solicitudes de servicio relacionadas con el usuario autenticado y un servicio municipal. El administrador y supervisor pueden cambiar su estado; el perfil administrativo solo consulta sus propias solicitudes.
- Recuperación de contraseña mediante enlace firmado y de un solo uso.
- Panel con navegación e indicadores acordes al perfil.

Después de aplicar las migraciones, crea la primera cuenta con `python manage.py createsuperuser`. Esa cuenta puede administrar usuarios y asignar perfiles en **Panel de gestión → Usuarios**. Para las cuentas siguientes, registra un correo válido, ya que el flujo de recuperación depende de él.

En desarrollo, el correo de recuperación se imprime en la consola. Para enviarlo desde AWS, configura el proveedor SMTP en el entorno de ejecución, sin subir credenciales al repositorio:

```dotenv
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=usuario-smtp
EMAIL_HOST_PASSWORD=secreto-smtp
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=no-reply@example.com
```

Para un integrante, la implementación incluye los dos mantenedores y una transacción mínimos. Si el equipo tiene más integrantes, agrega dos mantenedores y una transacción por cada integrante adicional, según la pauta.

Ejecuta las validaciones con:

```powershell
python manage.py migrate
python manage.py check
python manage.py test
```