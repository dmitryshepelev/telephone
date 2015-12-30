import datetime
import uuid
from django.contrib.auth.models import User
from django.db import models
from telephone import settings


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	user_key = models.CharField(max_length=50, default='')
	secret_key = models.CharField(max_length=50, default='')
	profile_email = models.EmailField(max_length=30, default='')
	profile_password = models.CharField(max_length=30, default='')
	profile_phone_number = models.CharField(max_length=20, default='')
	uid = models.CharField(max_length=50, default='')
	token = models.CharField(max_length=50, default='')
	customer_number = models.CharField(max_length=10, default='')
	date_subscribe_ended = models.DateTimeField(null=True)
	sip = models.IntegerField(null=True)

	class Meta:
		app_label = 'main_app'

	def __unicode__(self):
		return str(self.user)


class Callee(models.Model):
	sip = models.CharField(max_length=20, unique=True)
	description = models.CharField(max_length=1000, null=True)
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
	call_type = models.CharField(max_length=40, null=True)
	user_profile = models.ForeignKey(UserProfile)
	callee = models.ForeignKey(Callee)
	record_filename = models.CharField(max_length=100, null=True, default=None)

	class Meta:
		app_label = 'main_app'


class TransactionStatus(models.Model):
	value = models.CharField(max_length=20)

	class Meta:
		app_label = 'main_app'


class SubscribeTransaction(models.Model):
	transact_id = models.CharField(max_length=40, null=False)
	receiver = models.CharField(max_length=20, null=False, default=settings.W_NUMBER)
	form_comments = models.CharField(max_length=50, null=True)
	short_dest = models.CharField(max_length=50, null=True)
	quickpay_form = models.CharField(max_length=6, default='shop', null=False)
	targets = models.CharField(max_length=150, null=True)
	sum = models.FloatField()
	payment_type = models.CharField(max_length=2, null=False, default='PC')
	duration = models.IntegerField()
	expiration_date = models.DateTimeField(null=True)
	creation_date = models.DateTimeField(null=False, default=datetime.datetime.now())
	is_archive = models.BooleanField(null=False, default=False)
	user_profile = models.ForeignKey(UserProfile)
	status = models.ForeignKey(TransactionStatus)

	class Meta:
		app_label = 'main_app'


class ProfileRequestTransaction(models.Model):
	transact_id = models.CharField(max_length=40, null=False, default=str(uuid.uuid4()))
	creation_date = models.DateTimeField(null=False, default=datetime.datetime.now())
	email = models.EmailField(max_length=30, null=False)
	username = models.EmailField(max_length=50, null=True)
	status = models.ForeignKey(TransactionStatus)

	class Meta:
		app_label = 'main_app'


class RedirectNumbers(models.Model):
	number = models.CharField(max_length=20, null=False)
	user_profile = models.ForeignKey(UserProfile)

	class Meta:
		app_label = 'main_app'