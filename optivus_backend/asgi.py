"""
ASGI config for optivus_backend project.

It exposes the ASGI callable as a module-level variable named `application`.
"""

import os
from django.core.asgi import get_asgi_application

# Correct settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'optivus_backend.settings')

application = get_asgi_application()
