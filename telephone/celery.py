from __future__ import absolute_import
from celery import Celery


app = Celery('telephone', broker='amqp://guest@localhost//')

app.conf.update(
	CELERY_IMPORTS=('telephone.tasks',)
)