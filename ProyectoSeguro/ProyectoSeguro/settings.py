from dotenv import load_dotenv
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'AdmiSer',
    'captcha',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ProyectoSeguro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ProyectoSeguro.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
#  }
DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.mysql',
         'NAME': os.getenv('DB_NAME'),
         'USER': os.getenv('DB_USER'),
         'PASSWORD': os.getenv('DB_PASSWORD'),
         'HOST':os.getenv('DB_HOST'),
         'PORT':os.getenv('PORT'),
     }
 }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [ BASE_DIR / 'AdmiSer' / 'static' ]


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'bloqueo_login',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASS')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Evitar que la aplicación sea cargada en un iframe (clickjacking)
X_FRAME_OPTIONS = 'DENY'  # Impide que tu sitio se cargue dentro de un iframe en otro sitio

# Impide que los navegadores intenten adivinar el tipo de contenido (helpful for XSS)
SECURE_CONTENT_TYPE_NOSNIFF = True

# # Impide que los navegadores realicen "sniffing" de los archivos y contenido
SECURE_BROWSER_XSS_FILTER = True

# Protege las respuestas HTTP para que no se puedan modificar a través de ciertos tipos de ataques.
SECURE_REFERRER_POLICY = 'same-origin'

# Limita la duración de la sesión
SESSION_COOKIE_AGE = 180

# Impide que la cookie de sesión se envíe a otros dominios
SESSION_COOKIE_DOMAIN = None  # Esto asegura que la cookie solo sea accesible desde el dominio actual.

# Hacer que la cookie de sesión tenga solo acceso HTTP (no accesible a través de JavaScript)
SESSION_COOKIE_HTTPONLY = True  # Esto evita que la cookie sea accesible a través de JavaScript.

# Fuerza el uso de HTTPS
#SECURE_SSL_REDIRECT = True  # Redirige automáticamente todo el tráfico HTTP a HTTPS

# Asegura que la cookie de sesión solo se envíe a través de HTTPS
SESSION_COOKIE_SECURE = True  # Solo se enviará por HTTPS

# Hacer que las cookies de sesión sean más seguras:
CSRF_COOKIE_SECURE = True  # Solo envía la cookie CSRF en conexiones HTTPS

CSRF_COOKIE_DOMAIN = '.admiser.com'  # incluye subdominios
SESSION_COOKIE_DOMAIN = ".admiser.com"


CSRF_TRUSTED_ORIGINS = [
    "https://admiser.com",
    "https://www.admiser.com"  # si también tienes esta versión con 'www'
]
