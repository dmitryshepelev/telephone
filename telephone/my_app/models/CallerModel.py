from django.db import models

from telephone.my_app.models.ModelBase import ModelBase
from telephone.my_app.models.PBXModel import PBX


class Caller(ModelBase):
	sip = models.CharField(max_length = 20)
	description = models.CharField(max_length = 1000, null = True)
	pbx = models.ForeignKey(PBX, to_field = 'guid')

	class Meta:
		app_label = 'my_app'
