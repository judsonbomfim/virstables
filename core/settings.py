from pathlib import Path
import os
from django.contrib.messages import constants as messages
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    h.strip() for h in os.getenv('ALLOWED_HOSTS', '').split(',')
    if h.strip()
]

CSRF_TRUSTED_ORIGINS = [
    a.strip().replace('\\x3a', ':') for a in os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',')
    if a.strip()
]

DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',
    'rest_framework',
    'sass_processor',
    'widget_tweaks',
    'apps.cavalo.apps.CavaloConfig',
    'apps.emails.apps.EmailsConfig',
    'apps.home.apps.HomeConfig',
    'apps.leilao.apps.LeilaoConfig',
    'apps.site_config.apps.SiteConfigConfig',
    'apps.users.apps.UsersConfig',
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

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.site_config.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASE_URL = os.getenv('DATABASE_URL', f'postgres://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@db:5432/{os.getenv("DB_NAME")}')

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': os.getenv('DB_PORT'),
    }
}

AUTHENTICATION_BACKENDS = [
    'apps.users.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
]

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
DATE_INPUT_FORMATS = ('%d/%m/%Y',)
USE_I18N = True
USE_L10N = True
USE_TZ = False

DATE_FORMAT = '%d/%m/%Y'

DATA_UPLOAD_MAX_NUMBER_FILES = 1000

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Expirar sessão em 10h
SESSION_COOKIE_AGE = 36000


PAINEL_TITLE = str(os.getenv('PAINEL_TITLE'))
URL_SITE = str(os.getenv('URL_SITE'))
URL_PAINEL = str(os.getenv('URL_PAINEL'))
URL_CDN = 'https://'+str(os.getenv('URL_CDN'))


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'core/static'),
]
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field


# CELERY
REDIS_URL = os.getenv('REDIS_URL')
CELERY_BROKER_URL = str(os.getenv('CELERY_BROKER_URL'))
CELERY_RESULT_BACKEND = str(os.getenv('CELERY_RESULT_BACKEND'))
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_BEAT_SYNC_EVERY = None
CELERY_TIMEZONE = os.getenv('CELERY_TIMEZONE')

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('REDIS_URL', 'redis://redis:6379/0'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}



MESSAGE_TAGS = {
    messages.DEBUG: 'primary',
    messages.ERROR: 'danger',
    messages.SUCCESS: 'success',
    messages.INFO: 'info',
    messages.WARNING: 'warning',
}

# E-mail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = str(os.getenv('EMAIL_HOST'))
EMAIL_PORT = 587
EMAIL_HOST_USER = str(os.getenv('EMAIL_HOST_USER'))
EMAIL_HOST_PASSWORD = str(os.getenv('EMAIL_HOST_PASSWORD'))
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = str(os.getenv('DEFAULT_FROM_EMAIL'))


# # Configurações AWS
# AWS_ACCESS_KEY_ID = str(os.getenv('AWS_ACCESS_KEY_ID'))
# AWS_SECRET_ACCESS_KEY = str(os.getenv('AWS_SECRET_ACCESS_KEY'))
# AWS_STORAGE_BUCKET_NAME = str(os.getenv('AWS_STORAGE_BUCKET_NAME'))
# AWS_S3_REGION_NAME = str(os.getenv('AWS_S3_REGION_NAME'))
# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'
# AWS_S3_FILE_OVERWRITE = False  # Evita sobrescrever arquivos com mesmo nome
# AWS_DEFAULT_ACL = None  # Usa ACL do bucket (recomendado para django-storages 2.0+)

# # Configuração de armazenamento para arquivos estáticos e mídia
# STORAGES = {
#     'default': {
#         'BACKEND': 'core.storage_backends.PublicMediaStorage',
#         'OPTIONS': {
#             'location': 'media',  # Subpasta para arquivos de mídia
#             # 'default_acl': 'public-read',
#         },
#     },
#     'staticfiles': {
#         'BACKEND': 'core.storage_backends.StaticStorage',
#         'OPTIONS': {
#             'location': 'static',  # Subpasta para arquivos estáticos
#             # 'default_acl': 'public-read',
#         },
#     },
# }

# # URLs para arquivos estáticos e mídia
# STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
# MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'