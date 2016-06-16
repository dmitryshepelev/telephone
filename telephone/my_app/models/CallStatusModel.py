from django.db import models

from telephone.my_app.models.ModelBase import ModelBase


class CallStatus(ModelBase):
	name = models.CharField(max_length = 50)

	class Meta:
		app_label = 'my_app'
