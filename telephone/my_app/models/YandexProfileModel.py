from django.contrib.auth.models import User
from django.db import models

from telephone.my_app.models.ModelBase import ModelBase


class YandexProfile(ModelBase):
	yandex_email = models.EmailField(max_length = 50)
	yandex_password = models.CharField(max_length = 30)
	uid = models.CharField(max_length = 50)
	token = models.CharField(max_length = 50)
	user = models.OneToOneField(User, to_field = 'guid')

	class Meta:
		app_label = 'my_app'
