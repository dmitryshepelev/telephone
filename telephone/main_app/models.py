from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	user_key = models.CharField(max_length=50, default='')
	secret_key = models.CharField(max_length=50, default='')
	profile_email = models.EmailField(max_length=30, default='')
	profile_password = models.CharField(max_length=30, default='')
	uid = models.CharField(max_length=50, default='')
	token = models.CharField(max_length=50, default='')

	class Meta:
		app_label = 'main_app'


class Call(models.Model):
	call_id = models.CharField(max_length=30, null=False)
	sip = models.CharField(max_length=20)
	date = models.DateTimeField()
	destination = models.CharField(max_length=30)
	description = models.CharField(max_length=100)
	disposition = models.CharField(max_length=20)
	bill_seconds = models.IntegerField()
	cost = models.FloatField()
	bill_cost = models.FloatField()
	currency = models.CharField(max_length=20)
	user_profile = models.ForeignKey(UserProfile)

	class Meta:
		app_label = 'main_app'