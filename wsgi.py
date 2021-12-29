"""
WSGI config for computing_environment project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if os.environ.get("ENV") == 'production':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.production')
elif os.environ.get("ENV") == 'staging':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.staging')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.development')
    

application = get_wsgi_application()
