import hashlib
import time
import datetime
from telephone import settings


class Parameters():
	def __init__(self):
		self.__params = {
			# Display anonymous calls: 0 - No; 1 - Yes
			'anonymous': 1,
			# New clients only: 0 - No; 1 - Yes
			'firstTime': 0,
			# Start date: 'd.m.Y'
			'from': datetime.datetime.strptime(datetime.datetime.now().strftime(settings.DATETIME_FORMAT), settings.DATETIME_FORMAT),
			# Callee number
			'fromNumber': '',
			# Call status: 0 - all calls; 1 - missed; 2 - accepted
			'state': 0,
			# End date (inclusively): 'd.m.Y'
			'to': datetime.datetime.strptime(datetime.datetime.now().strftime(settings.DATETIME_FORMAT), settings.DATETIME_FORMAT),
			# Call responder number
			'toAnswer': '',
			# Call destination number
			'toNumber': '',
			# Schema number
			'tree': '',
			# Call type: 0 - all calls; 1 - incoming; 2 - upcoming; 3 - inner
			'type': 0,
			# User code
			'user': ''
		}

	@staticmethod
	def get_hash_string(params):
		"""
		Calculates md5 hash string
		:return: md5 hash string
		"""
		return hashlib.md5('%s%s' % (''.join('{}+'.format(value) for key, value in sorted(params.items())), settings.S_KEY,)).hexdigest()

	def set_params(self, params):
		"""
		Sets parameters
		:param params: array of parameters
		:return: None
		"""
		for key, value in params.items():
			self.__params[key] = params[key]

	def get_request_string(self):
		"""
		Generate request string from parameters
		:return: request string
		"""
		return '?%shash=%s' % (''.join('{}={}&'.format(key, value) for key, value in sorted(self.__params.items())), self.get_hash_string(self.__params))

	def get_params(self):
		return self.__params