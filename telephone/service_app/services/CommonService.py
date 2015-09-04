import string
from django.utils import crypto
from telephone import settings


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
	def parse_csv(csv_string, cls):
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
			arr.append(cls(item.split(delimiter)))
		return arr