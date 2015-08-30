from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	user_key = models.CharField(max_length=50, default='')
	secret_key = models.CharField(max_length=50, default='')
	profile_email = models.CharField(max_length=30, default='')
	profile_password = models.CharField(max_length=30, default='')
	uid = models.CharField(max_length=50, default='')
	token = models.CharField(max_length=50, default='')

	class Meta:
		app_label = 'main_app'