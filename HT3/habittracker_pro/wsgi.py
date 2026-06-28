"""
WSGI config for habittracker_pro project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'habittracker_pro.settings')

application = get_wsgi_application()
