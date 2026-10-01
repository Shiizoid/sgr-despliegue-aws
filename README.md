# SGR La Serena

Aplicación web Django para administrar actividades y servicios municipales.

## Requisitos

- Python 3.12 o compatible con Django 6.1.
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

La aplicación estará disponible en `http://127.0.0.1:8000/` y el panel de administración en `http://127.0.0.1:8000/admin/`.

## Aplicaciones

- `actividades`: categorías y actividades, relacionadas mediante clave foránea.
- `servicios`: servicios municipales.

El archivo `.env` y los entornos virtuales están excluidos mediante `.gitignore`.