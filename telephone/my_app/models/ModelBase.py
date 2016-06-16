import hashlib
import json
import random
from collections import defaultdict
from time import timezone

from django.core import serializers
from django.db import models


class ModelBase(models.Model):
	guid = models.CharField(max_length = 40, db_index = True, unique = True)
	exist = models.BooleanField(default = True)
	creation_datetime = models.DateTimeField(default = timezone.now)
	last_edited_datetime = models.DateTimeField(default = timezone.now)

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