import hashlib
import json
import random
from collections import defaultdict
from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.contrib.auth.models import User
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Max
from django.utils import timezone

from telephone.my_app.utils import DateTimeUtil


class ModelBase(models.Model):
	guid = models.CharField(max_length = 40, db_index = True, unique = True)
	exist = models.BooleanField(default = True)
	creation_datetime = models.DateTimeField()
	last_edited_datetime = models.DateTimeField()

	class Meta:
		abstract = True

	def natural_key(self, *args, **kwargs):
		"""
		Returns natural key to serialize
		if {args} is specified, dicts are merged
		:return: {dict}
		"""
		default_keys = {
			'guid': self.guid,
			'creation_datetime': self.creation_datetime,
			'last_edited_datetime': self.last_edited_datetime
		}
		natural_keys = defaultdict(set)

		for d in args + (default_keys,):
			for key, value in d.iteritems():
				natural_keys[key] = value

		return natural_keys

	def serialize(self, format = 'json', include_fields = (), exclude_fields = (), use_natural_foreign_keys = True,
					use_natural_primary_keys = True):
		"""
		Serialize object
		:param format: format to serialize
		:param include_fields: fields to include. All fields are serialized by default
		:param exclude_fields: fields to exclude. 'exist' field is excluded by default
		:param use_natural_primary_keys:
		:param use_natural_foreign_keys:
		:return:
		"""
		options = {
			'use_natural_foreign_keys': use_natural_foreign_keys,
			'use_natural_primary_keys': use_natural_primary_keys
		}

		if include_fields:
			options['fields'] = include_fields

		serialized = json.loads(
			serializers.serialize(format, [self], **options))

		serialized = serialized[0].get('fields', {})

		exclude_fields = tuple(set(exclude_fields) | {'exist'})
		for key in exclude_fields:
			if key in serialized.keys():
				serialized.__delitem__(key)

		return serialized

	def save(self, force_insert = False, force_update = False, using = None, update_fields = None):
		"""
		Overrides base save method
		:param force_insert:
		:param force_update:
		:param using:
		:param update_fields:
		:return:
		"""
		if not self.guid:
			self.guid = hashlib.sha1(str(random.random())).hexdigest()

		current_datetime = timezone.now()

		if not self.creation_datetime:
			self.creation_datetime = current_datetime

		self.last_edited_datetime = current_datetime

		super(ModelBase, self).save(force_insert, force_update, using, update_fields)

	def get_protected_fields(self):
		"""
		Returns the fields which shouldn't be changed
		:return: {tuple}
		"""
		return 'id', 'guid', 'exist', 'creation_datetime', 'last_edited_datetime'

	def update(self, data):
		"""
		Update object by props
		:return:
		"""
		for prop in data:
			if prop in self.get_protected_fields():
				continue

			if prop in self.__dict__.keys():
				self.__dict__[prop] = data.get(prop)

	def full_clean(self, exclude=None, validate_unique=True):
		"""
		Validate model fields
		:param exclude:
		:param validate_unique:
		"""
		exclude = tuple(set(exclude or tuple()) | {'guid'})
		super(ModelBase, self).full_clean(exclude = exclude, validate_unique = validate_unique)


class PBX(ModelBase):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	user_key = models.CharField(max_length = 20)
	secret_key = models.CharField(max_length = 20)
	phone_number = models.CharField(max_length = 20)
	customer_number = models.CharField(max_length = 6)
	sip = models.IntegerField(null = True)

	class Meta:
		app_label = 'my_app'


class CallerManager(models.Manager):
	"""
	Caller manager
	"""
	def create_caller(self, sip, pbx_id, call_datetime, description = None):
		"""
		Create a callee entity if not exist. Else update date of first call
		:param callee: Callee instance
		:return: Callee instance
		"""
		try:
			# Get existing callee entity by its phone number
			exs_callee = self.get(pbx_id = pbx_id, sip = sip)
			# check if existing callee first call date over current callee first call date
			# If true that means current call of callee was before existing and existing needs to be updated with a new date
			if exs_callee.first_call_datetime > call_datetime:
				exs_callee.first_call_datetime = call_datetime
				exs_callee.save()
			# Else just return existing callee
			return exs_callee
		except ObjectDoesNotExist as e:
			# Create a new callee
			caller = self.create(
				sip = sip,
				description = description,
				pbx_id = pbx_id
			)
			return caller


class Caller(ModelBase):
	sip = models.CharField(max_length = 20)
	description = models.CharField(max_length = 1000, null = True)
	pbx = models.ForeignKey(PBX, to_field = 'guid')
	first_call_datetime = models.DateTimeField()

	objects = CallerManager()

	class Meta:
		app_label = 'my_app'


class CallStatus(ModelBase):
	name = models.CharField(max_length = 50)

	class Meta:
		app_label = 'my_app'


class CallType(ModelBase):
	INCOMING = 'incoming'
	INTERNAL = 'internal'
	OUTGOING = 'outgoing'

	name = models.CharField(max_length = 8)

	class Meta:
		app_label = 'my_app'


class PBXCallManager(models.Manager):
	"""
	PBXCall manager
	"""
	def create_call(self, call, pbx):
		"""
		Create pbx call
		:return:
		"""
		if (isinstance(call.destination, str) or isinstance(call.destination, unicode)) and 'w00e' in call.destination:
			call.destination = call.destination[4:]

		if (isinstance(call.sip, str) or isinstance(call.sip, unicode)) and 'w00e' in call.sip:
			call.sip = call.sip[4:]

		caller = Caller.objects.create_caller(call.sip, pbx.guid, call.date, call.description)

		call = PBXCall(
			call_id = call.call_id,
			date = call.date,
			destination = call.destination,
			disposition = call.disposition,
			bill_seconds = call.bill_seconds,
			cost = call.cost,
			bill_cost = call.bill_cost,
			currency = call.currency,
			pbx_id = pbx.id,
			caller = caller,
			call_type = call.call_type
		)
		# create Call Instance
		return call.save()


class PBXCall(ModelBase):
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
	pbx = models.ForeignKey(PBX, to_field = 'guid')

	objects = PBXCallManager()

	class Meta:
		app_label = 'my_app'


class WidgetScript(ModelBase):
	pbx = models.ForeignKey(PBX, to_field = 'guid', on_delete = models.CASCADE)

	class Meta:
		app_label = 'my_app'


class IncomingCallInfo(ModelBase):
	caller_id = models.CharField(max_length = 30)
	called_did = models.CharField(max_length = 30)
	call_start = models.DateTimeField()
	expiration_date = models.DateTimeField()
	script = models.ForeignKey(WidgetScript, to_field = 'guid')

	class Meta:
		app_label = 'my_app'


class RedirectNumber(ModelBase):
	number = models.CharField(max_length = 20)
	pbx = models.ForeignKey(PBX, to_field = 'guid', on_delete = models.CASCADE)

	class Meta:
		app_label = 'my_app'


class RegisteredCallback(ModelBase):
	date = models.DateTimeField()
	caller = models.CharField(max_length = 20)
	destination = models.CharField(max_length = 20)
	is_pending = models.BooleanField(default = True)
	pbx = models.ForeignKey(PBX, to_field = 'guid', on_delete = models.CASCADE)

	class Meta:
		app_label = 'my_app'


class SubscriptionStatus(ModelBase):
	ACTIVE = 'active'
	ENDED = 'ended'
	PENDING = 'pending'
	STOPPED = 'stopped'

	name = models.CharField(max_length = 7)

	class Meta:
		app_label = 'my_app'


class Subscription(ModelBase):
	start_date = models.DateTimeField()
	duration = models.PositiveIntegerField()
	status = models.ForeignKey(SubscriptionStatus, on_delete = models.CASCADE, to_field = 'guid')
	user = models.ForeignKey(User, on_delete = models.CASCADE)

	class Meta:
		app_label = 'my_app'

	def get_end_date(self):
		"""
		Returns the date of the subscription end
		:return:
		"""
		return self.start_date + relativedelta(days = self.duration)

	def days_remain(self):
		"""
		Return the number of days that remain to the end of the subscription
		:return:
		"""
		return (self.get_end_date() - DateTimeUtil.convert_to_UTC(datetime.now())).days


class YandexProfile(ModelBase):
	yandex_email = models.EmailField(max_length = 50)
	yandex_password = models.CharField(max_length = 30)
	uid = models.CharField(max_length = 50)
	token = models.CharField(max_length = 50)
	user = models.OneToOneField(User, on_delete = models.CASCADE)

	class Meta:
		app_label = 'my_app'


def get_current_subscription(self):
	"""
	Returns current subscription
	:param self:
	:return:
	"""
	return self.subscription_set.annotate(max_date = Max('creation_datetime')).last()


User.get_current_subscription = get_current_subscription
