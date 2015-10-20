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


class Callee(models.Model):
	sip = models.CharField(max_length=20, unique=True)
	description = models.CharField(max_length=100, null=True)
	first_call_date = models.DateTimeField(null=True)

	class Meta:
		app_label = 'main_app'


class Call(models.Model):
	call_id = models.CharField(max_length=30, null=False)
	date = models.DateTimeField(null=True)
	destination = models.CharField(max_length=30, null=True)
	disposition = models.CharField(max_length=20, null=True)
	bill_seconds = models.IntegerField(null=True)
	cost = models.FloatField(null=True)
	bill_cost = models.FloatField(null=True)
	currency = models.CharField(max_length=20, null=True)
	is_answered = models.BooleanField(default=True)
	user_profile = models.ForeignKey(UserProfile)
	callee = models.ForeignKey(Callee)

	class Meta:
		app_label = 'main_app'