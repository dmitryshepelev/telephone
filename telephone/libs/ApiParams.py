# coding=utf-8
from base64 import b64encode
import hashlib
import datetime
import hmac
import urllib

from telephone import settings
from telephone.service_app.services.CommonService import CommonService


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

	@property
	def params(self):
		"""
		Getter of __params
		:return: params
		"""
		return self.__params

	@property
	def api_version(self):
		"""
		Getter of __api_version
		:return: api_version
		"""
		return self.__api_version

	def __get_domain_url(self, method):
		"""
		Generate high-level url to request
		:param method: api method name
		:return: domain url as 'https://domain/api_version/method'
		"""
		return '%s%s%s?' % (self.__domain, self.__api_version, method)

	def get_request_string(self, method):
		"""
		Generate full request string from parameters
		:return: request string
		"""
		return '%s%s' % (self.__get_domain_url(method), CommonService.get_params_string(self.__params))

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

	def clean_params(self):
		self.__params = {}