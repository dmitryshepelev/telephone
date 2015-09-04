import string
from django.utils import crypto


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