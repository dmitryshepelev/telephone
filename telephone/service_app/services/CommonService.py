import string
import datetime

from django.utils import crypto
from enum import Enum
from telephone import settings


class Constants(Enum):
	CUR_DATE_DAY_START_STR = datetime.datetime.now().strftime(settings.DATETIME_FORMAT_START)
	CUR_DATE_DAY_END_STR = datetime.datetime.now().strftime(settings.DATETIME_FORMAT_END)


class CallsConstants(Enum):
	ANSWERED = 'answered'
	INCOMING = 'incoming'


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

	@staticmethod
	def is_dates_equals(date1, date2, with_sec):
		"""
		Check if the dates are equals with error
		:param date1: DateTime
		:param date2: DateTime
		:param with_sec: comparison by secs
		:return: Boolean
		"""
		if with_sec:
			return abs(date1 - date2).seconds <= settings.TIME_CORRECTION_SEC
		return date1.date() == date2.date() and date1.hour == date2.hour and abs(date1.minute - date2.minute) <= settings.TIME_CORRECTION_MIN