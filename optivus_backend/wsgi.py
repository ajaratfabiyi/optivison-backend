"""
WSGI config for optivus_backend project.

It exposes the WSGI callable as a module-level variable named `application`.
"""

import os
from django.core.wsgi import get_wsgi_application

# Correct settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'optivus_backend.settings')

application = get_wsgi_application()
