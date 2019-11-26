from __future__ import absolute_import

import django
import redis
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'money_reminder.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

django.setup()

app = Celery('"money_reminder')

app.conf.broker_url = "redis://localhost:6379/0"
app.conf.result_backend = "redis://localhost:6379/0"


app.config_from_object('django.conf:settings')
app.autodiscover_tasks(settings.INSTALLED_APPS, force=True)