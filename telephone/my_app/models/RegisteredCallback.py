from time import timezone

from django.db import models

from telephone.my_app.models.ModelBase import ModelBase
from telephone.my_app.models.PBXModel import PBX


class RegisteredCallback(ModelBase):
	date = models.DateTimeField(default = timezone.now)
	caller = models.CharField(max_length = 20)
	destination = models.CharField(max_length = 20)
	is_pending = models.BooleanField(default = True)
	pbx = models.ForeignKey(PBX, to_field = 'guid', on_delete = models.CASCADE)

	class Meta:
		app_label = 'my_app'
