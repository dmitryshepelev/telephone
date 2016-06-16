from django.db import models

from telephone.my_app.models.ModelBase import ModelBase


class SubscriptionStatus(ModelBase):
	ACTIVE = 'active'
	ENDED = 'ended'
	PENDING = 'pending'
	STOPPED = 'stopped'

	STATUSES = (ACTIVE, ENDED, PENDING, STOPPED)

	name = models.CharField(max_length = 7, choices = STATUSES)

	class Meta:
		app_label = 'my_app'
