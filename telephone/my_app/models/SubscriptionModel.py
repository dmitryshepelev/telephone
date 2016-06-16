from django.contrib.auth.models import User
from django.db import models

from telephone.my_app.models.ModelBase import ModelBase
from telephone.my_app.models.SubscriptionStatusModel import SubscriptionStatus


class Subscription(ModelBase):
	start_date = models.DateTimeField()
	duration = models.PositiveIntegerField()
	status = models.ForeignKey(SubscriptionStatus, on_delete = models.CASCADE, to_field = 'guid')
	user = models.ForeignKey(User, on_delete = models.CASCADE)

	class Meta:
		app_label = 'my_app'
