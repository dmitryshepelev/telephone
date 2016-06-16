from django.db import models

from telephone.my_app.models.ModelBase import ModelBase
from telephone.my_app.models.PBXModel import PBX


class RedirectNumber(ModelBase):
	number = models.CharField(max_length = 20)
	pbx = models.ForeignKey(PBX, to_field = 'guid', on_delete = models.CASCADE)

	class Meta:
		app_label = 'main_app'
