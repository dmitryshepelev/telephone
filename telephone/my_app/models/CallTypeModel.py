from django.db import models

from telephone.my_app.models.ModelBase import ModelBase


class CallType(ModelBase):
	INCOMING = 'incoming'
	INTERNAL = 'internal'
	OUTGOING = 'outgoing'

	TYPES = (INCOMING, INTERNAL, OUTGOING)

	name = models.CharField(max_length = 8, choices = TYPES)

	class Meta:
		app_label = 'my_app'
