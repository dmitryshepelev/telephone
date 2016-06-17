import hashlib
import hmac
import json
import urllib
from collections import OrderedDict

import requests

from telephone import settings
from telephone.my_app.services.ServiceBase import ServiceBase, ServiceResultError


class PBXService(ServiceBase):
	def __init__(self, pbx_model):
		self.__pbx = pbx_model

		self.__host = settings.PBX['host']
		self.__version = settings.PBX['version']
		self.__method = ''

	def __get_url(self):
		"""
		Creates url to request
		:param method:
		:return:
		"""
		return '{host}{version}{method}'.format(host = self.__host, version = self.__version, method = self.__method)

	def __sha_encode(self, request_string):
		"""
		Encodes with sha
		:param secret_key:
		:param kwargs:
		:return:
		"""
		path = '/{version}{method}'.format(version = self.__version, method = self.__method)
		return hmac.new(
			self.__pbx.secret_key.encode(),
			'%s%s%s' % (path, request_string, hashlib.md5(request_string).hexdigest()), hashlib.sha1
		).hexdigest().encode('base64')

	def __get_request_string(self, **kwargs):
		"""
		Creates request string
		:param kwargs:
		:return:
		"""
		return urllib.urlencode(OrderedDict(sorted(kwargs.items())))

	def __get_sign(self, **kwargs):
		"""
		Get authorization sign
		:return:
		"""
		request_string = self.__get_request_string(**kwargs)
		return self.__sha_encode(request_string)

	def __get_authorization_header(self, sign):
		"""
		Returns authorization header
		:return:
		"""
		return {'Authorization': '%s:%s' % (self.__pbx.user_key, sign)}

	def get_balance(self):
		"""
		Returns pbx balance
		:return:
		"""
		self.__method = settings.PBX['urls']['balance']
		url = self.__get_url()

		sign = self.__get_sign()
		headers = self.__get_authorization_header(sign)

		response = requests.get(url, headers = headers)
		content = response.content

		if response.ok:
			return json.loads(content)['balance']

		raise ServiceResultError(response.status_code, content)
