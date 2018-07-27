from CriteriBackend.settings.base import *

MODULE='Test'
TEST_DATA_DIR = os.path.join(BASE_DIR, 'TestData')

DEBUG = os.environ.get('DEBUG', '')
SECRET_KEY = os.environ.get('SECRET_KEY', '')

ALLOWED_HOSTS = []
INSTALLED_APPS += []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'test_db.sqlite3'),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")