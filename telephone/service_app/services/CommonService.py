import os
import string
import datetime

from django.utils import crypto

from telephone import settings
from telephone.classes.ServiceResponse import ServiceResponse


class Constants():
	def __init__(self):
		pass

	CUR_DATE_DAY_START_STR = datetime.datetime.now().strftime(settings.DATETIME_FORMAT_START)
	CUR_DATE_DAY_END_STR = datetime.datetime.now().strftime(settings.DATETIME_FORMAT_END)


class CallsConstants():
	def __init__(self):
		pass

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

	@staticmethod
	def write_temp_file(file_instance):
		"""
		Write the file to the filesystem
		:param file_instance: File instance
		:return: path to the file
		"""
		folder_path = 'static/temp'
		file_path = '%s/%s' % (folder_path, file_instance.filename)
		try:
			if not os.path.exists(folder_path):
				os.makedirs(folder_path)
			open(file_path, 'wb').write(file_instance.content)
			return ServiceResponse(True, data=file_path)
		except Exception as e:
			return ServiceResponse(False, message=e.message, data=file_path)

	@staticmethod
	def delete_temp_file(filename):
		"""
		Delete temp file from the filesystem
		:param filename: name of the file
		:return:
		"""
		os.remove('static/temp/' + filename)