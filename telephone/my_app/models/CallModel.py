from django.db import models

from telephone.my_app.models.CallStatusModel import CallStatus
from telephone.my_app.models.CallTypeModel import CallType
from telephone.my_app.models.CallerModel import Caller
from telephone.my_app.models.ModelBase import ModelBase


class Call(ModelBase):
	call_id = models.CharField(max_length = 30)
	date = models.DateTimeField(null = True)
	destination = models.CharField(max_length = 30, null = True)
	bill_seconds = models.IntegerField(null = True)
	cost = models.FloatField(null = True)
	bill_cost = models.FloatField(null = True)
	currency = models.CharField(max_length = 20, null = True)
	record_filename = models.CharField(max_length = 100, null = True, default = None)
	caller = models.ForeignKey(Caller, to_field = 'guid', on_delete = models.CASCADE)
	status = models.ForeignKey(CallStatus, to_field = 'guid', on_delete = models.CASCADE)
	type = models.ForeignKey(CallType, to_field = 'guid', on_delete = models.CASCADE)

	class Meta:
		app_label = 'main_app'
