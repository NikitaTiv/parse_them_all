import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tesseract_api.settings')

app = Celery('tesseract_api')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
