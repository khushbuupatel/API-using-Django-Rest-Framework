import os
import sys
import django
from unipath import Path
from django_api import settings

# create django setup to run this script using the django setup
sys.path.append(Path(settings.BASE_DIR).parent)
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_api.settings'
django.setup()
