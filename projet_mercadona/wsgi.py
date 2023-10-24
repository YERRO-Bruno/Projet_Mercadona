"""
WSGI config for projet_mercadona project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projet_mercadona.settings")
django.setup()
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
