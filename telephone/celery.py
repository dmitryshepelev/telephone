from __future__ import absolute_import

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telephone.settings')

from django.conf import settings

schedule_app = Celery('telephone', broker='amqp://localhost:8001')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
schedule_app.config_from_object('django.conf:settings')
schedule_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@schedule_app.task(bind=True)
def debug_task(self, v):
	print(v)
	print('Request: {0!r}'.format(self.request))