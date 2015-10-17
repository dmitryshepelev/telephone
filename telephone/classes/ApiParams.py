# coding=utf-8
from base64 import b64encode
import hashlib
import datetime
import hmac
import urllib

from telephone import settings


class ApiParams(object):

	def __init__(self, params=None):
		self.__domain = settings.API_URLS['api']['host']
		self.__api_version = settings.API_URLS['api']['api_version']
		self.__params = {
			# Start date: 'd.m.Y' *Required*
			'start': datetime.datetime.now().strftime(settings.DATETIME_FORMAT_START),
			# End date (inclusively): 'd.m.Y' *Required*
			'end': datetime.datetime.now().strftime(settings.DATETIME_FORMAT_END),
		}
		self.set_params(params)

	@property
	def start(self):
		"""
		Getter of Start param
		:return: DateTime
		"""
		return self.__params['start']

	@property
	def end(self):
		"""
		Getter of End param
		:return: DateTime
		"""
		return self.__params['end']

	def __get_params_string(self):
		"""
		Generate request string from parameters
		:return: request string
		"""
		return urllib.urlencode(sorted(filter(lambda item: item[1], self.__params.items())))

	def __sha_encode(self, method_name, secret_key):
		"""
		Encode string with sha1 algorithm with secret key
		:param method_name: api method name
		:param secret_key: user secret key to api access
		:return: sha1 encoded string
		"""
		params_string = self.__get_params_string()
		return hmac.new(secret_key.encode(), '%s%s%s%s' % (self.__api_version, method_name, params_string, hashlib.md5(params_string).hexdigest()), hashlib.sha1).hexdigest()

	def __get_domain_url(self, method):
		"""
		Generate high-level url to request
		:param method: api method name
		:return: domain url as 'https://domain/api_version/method'
		"""
		return '%s%s%s?' % (self.__domain, self.__api_version, method)

	def get_sign(self, method, secret_key):
		"""
		Generate authorization sigh
		:param method: api method
		:param secret_key: api secret key
		:return: base64 encoded string
		"""
		sha_string = self.__sha_encode(method, secret_key)
		return b64encode(sha_string)

	def get_request_string(self, method):
		"""
		Generate full request string from parameters
		:return: request string
		"""
		return '%s%s' % (self.__get_domain_url(method), self.__get_params_string())

	def set_params(self, params):
		"""
		Sets parameters
		:param params: array of parameters
		:return: None
		"""
		if params:
			for key, value in params.items():
				if value:
					if key == 'start':
						value = datetime.datetime.strptime(value, settings.DATE_CLIENT_FORMAT).strftime(settings.DATETIME_FORMAT_START)
					elif key == 'end':
						value = datetime.datetime.strptime(value, settings.DATE_CLIENT_FORMAT).strftime(settings.DATETIME_FORMAT_END)
					self.__params[key] = value