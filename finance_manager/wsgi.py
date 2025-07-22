"""
WSGI config for finance_manager project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# Add your project directory to the Python path
project_home = '/home/davidentonu/Finance-manager'  # <–– adjust 'davidentonu' if your PA username is different
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Ensure the settings module is set correctly
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_manager.settings')

application = get_wsgi_application()
