import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agenda.settings")

app = Celery("agenda")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
