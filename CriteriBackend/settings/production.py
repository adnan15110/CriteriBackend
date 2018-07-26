from CriteriBackend.settings.base import *
import dj_database_url
from decouple import config

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = []

INSTALLED_APPS += []

MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware',]


SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'