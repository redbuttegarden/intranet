from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q5#6qf*_qxwch$=&u)e7r3brp$6z5ceia@xbza7uo7=2sg_47&'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Needed to prevent ValueErrors while testing: https://docs.djangoproject.com/en/3.0/ref/contrib/staticfiles/#django.contrib.staticfiles.storage.ManifestStaticFilesStorage.manifest_strict
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

try:
    from .local import *
except ImportError:
    pass
