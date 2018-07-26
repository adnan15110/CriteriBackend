from CriteriBackend.settings.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6nehypd6v$a923!9)+6eqqpdl22swn-0_b=t6*kyf_q8e6o&l9'

DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS += []

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'test_db.sqlite3'),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
