from base64 import b64encode
import hashlib
import datetime

from telephone import settings


class Parameters():
	def __init__(self, params):
		self.__secret_key = settings.S_KEY
		self.__domain = settings.API_URLS['base_api_url']
		self.__api_version = settings.API_URLS['api_version']
		self.__params = params

	def __get_request_string(self):
		"""
		Generate request string from parameters
		:return: request string
		"""
		return '?%s' % (''.join('{}={}&'.format(key, value) for key, value in sorted(self.__params.items()))[:-1])

	def __sha_encode(self, method_name):
		request_string = self.__get_request_string()
		sha1 = hashlib.sha1()
		sha1.update('%s%s%s%s' % (self.__api_version, method_name, request_string, hashlib.md5(request_string)))
		return sha1.hexdigest()

	def get_sign(self, method_name):
		sha_str = self.__sha_encode(method_name)
		return b64encode(sha_str)

	def set_params(self, params):
		"""
		Sets parameters
		:param params: array of parameters
		:return: None
		"""
		for key, value in params.items():
			self.__params[key] = params[key]


class CallsParameters(Parameters):
	def __init__(self):
		__params = {
			# Start date: 'd.m.Y' *Required*
			'start': datetime.datetime.strptime(datetime.datetime.now().strftime(settings.DATETIME_FORMAT), settings.DATETIME_FORMAT),
			# End date (inclusively): 'd.m.Y' *Required*
			'end': datetime.datetime.strptime(datetime.datetime.now().strftime(settings.DATETIME_FORMAT), settings.DATETIME_FORMAT),
			# Determine SIP number
			'sip': '',
			# Wasted cash
			'cost_only': '',
			# Call type: doesn't include - common; 'toll' - 800 number; ru495 - 495 number
			'type': ''
		}
		Parameters.__init__(self, __params)