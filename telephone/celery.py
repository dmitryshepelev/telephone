from __future__ import absolute_import
import os
from celery import Celery


os.environ['DJANGO_SETTINGS_MODULE'] = 'telephone.settings'

app = Celery('telephone', broker='amqp://guest@localhost//')

app.conf.update(
	CELERY_IMPORTS=('telephone.tasks',)
)