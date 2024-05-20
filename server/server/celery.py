import os
from time import sleep
from datetime import timedelta

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

app = Celery('main')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()