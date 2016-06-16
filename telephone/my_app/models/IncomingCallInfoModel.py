from django.db import models

from telephone.main_app.models import WidgetScript
from telephone.my_app.models.ModelBase import ModelBase


class IncomingCallInfo(ModelBase):
	caller_id = models.CharField(max_length = 30)
	called_did = models.CharField(max_length = 30)
	call_start = models.DateTimeField()
	expiration_date = models.DateTimeField()
	script = models.ForeignKey(WidgetScript, to_field = 'guid')

	class Meta:
		app_label = 'my_app'