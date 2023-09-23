"""
ASGI config for website_proj7_08_2023_bookFullpledge project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website_proj7_08_2023_bookFullpledge.settings')

application = get_asgi_application()
