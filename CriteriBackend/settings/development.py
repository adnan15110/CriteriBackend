from CriteriBackend.settings.base import *

TEST_DATA_DIR = os.path.join(BASE_DIR, 'TestData')
DEBUG = True
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6nehypd6v$a923!9)+6eqqpdl22swn-0_b=t6*kyf_q8e6o&l9'
ALLOWED_HOSTS = []
INSTALLED_APPS += []

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

AWS_ACCESS_KEY_ID = 'AKIAJZV5K4JX77QARCUQ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'criteri-static'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'

STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

DEFAULT_FILE_STORAGE = 'CriteriBackend.storage_backends.MediaStorage'