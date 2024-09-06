"""
WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

import os
import sys

# Add the project directory to the sys.path
project_home = '/home/Maneesh632/Ecommerce-website-with-django/project'
if project_home not in sys.path:
    sys.path.append(project_home)

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

 
application = get_wsgi_application()
