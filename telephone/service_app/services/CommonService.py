import string
import datetime

from django.utils import crypto
from enum import Enum
from telephone import settings


class Constants(Enum):
	CUR_DATE_DAY_START_STR = datetime.datetime.now().strftime(settings.DATETIME_FORMAT_START)
	CUR_DATE_DAY_END_STR = datetime.datetime.now().strftime(settings.DATETIME_FORMAT_END)


class CommonService():
	def __init__(self):
		pass

	@staticmethod
	def get_random_string(length, only_letters=False, only_digits=False):
		"""
		Generate random string form ascii letters and/or numbers
		:param length: length of string
		:param only_letters: boolean set if the string must contain only letters
		:param only_digits: boolean set if the string must contain only digits
		:return: string
		"""
		if only_letters:
			return crypto.get_random_string(length, string.ascii_letters)
		if only_digits:
			return crypto.get_random_string(length, string.digits)
		return crypto.get_random_string(length)

	@staticmethod
	def parse_csv(csv_string):
		"""
		Parse csv string into array of objects
		:param csv_string: data string
		:return: array of object
		"""
		arr = []
		delimiter = settings.DELIMITER
		csv_string = csv_string[:-1] if csv_string[-1] == '\n' else csv_string
		iter_csv = iter(csv_string.split('\n'))
		next(iter_csv)
		for item in iter_csv:
			arr.append(item.split(delimiter))
		return arr

	@staticmethod
	def parse_form_errors(errors):
		"""
		Parse form errors to the array of string
		:param errors: errors dictionary
		:return: dct - dictionary
		"""
		dct = {}
		for error in errors:
			for key, value in error.iteritems():
				dct[key] = value
		return dct