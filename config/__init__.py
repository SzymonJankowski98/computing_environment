from .base import *
import django_heroku
import os

if os.environ.get("ENV") == 'production':
    from .production import *
elif os.environ.get("ENV") == 'staging':
    from .staging import *
    django_heroku.settings(locals())
else:
    from .development import *