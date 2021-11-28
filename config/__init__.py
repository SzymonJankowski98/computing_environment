from .base import *
import os

if os.environ.get("ENV_NAME") == 'production':
    from .production import *
elif os.environ.get("ENV") == 'staging':
    from .staging import *
else:
    from .development import *