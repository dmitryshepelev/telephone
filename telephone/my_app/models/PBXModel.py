from django.contrib.auth.models import User
from django.db import models

from telephone.my_app.models.ModelBase import ModelBase


class PBX(ModelBase):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	user_key = models.CharField(max_length = 20)
	secret_key = models.CharField(max_length = 20)
	phone_number = models.CharField(max_length = 20)
	customer_number = models.CharField(max_length = 6)
	sip = models.IntegerField(null = True)

	class Meta:
		app_label = 'my_app'

