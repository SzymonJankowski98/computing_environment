from .base import ALLOWED_HOSTS
DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ALLOWED_HOSTS.append('10.0.2.2')