from django.contrib.auth.models import User
from django.db import models


class Schema(models.Model):
	schema_code = models.CharField(max_length=9)
	name = models.CharField(max_length=20)

	class Meta:
		app_label = 'main_app'

	def __unicode__(self):
		return u'%s' % self.name


class UserProfile(models.Model):
	schema = models.OneToOneField(Schema, on_delete=models.CASCADE)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	user_code = models.CharField(max_length=9)

	class Meta:
		app_label = 'main_app'