import hashlib
import hmac
import json
import urllib
from collections import OrderedDict, namedtuple

import requests
from django.utils import timezone

from telephone import settings
from telephone.my_app.services.ServiceBase import ServiceBase, ServiceResultError


StatParams = namedtuple('StatParams', ['start', 'end', 'status', 'call_type'])


class PBXService(ServiceBase):
	def __init__(self, pbx_model):
		self.__pbx = pbx_model

		self.__host = settings.PBX['host']
		self.__version = settings.PBX['version']
		self.__method = ''

	def __get_url(self, **kwargs):
		"""
		Creates url to request
		:param method:
		:return:
		"""
		url = '{host}{version}{method}'.format(host = self.__host, version = self.__version, method = self.__method)
		request_string = self.__get_request_string(**kwargs)
		return url + '?' + request_string if request_string else url

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

	def __get_stat(self, **kwargs):
		"""
		Gets stat specifiend on method
		:param method:
		:param kwargs:
		:return:
		"""
		start = kwargs.setdefault('start', timezone.now()).strftime(settings.DATETIME_FORMAT_START)
		end = kwargs.setdefault('end', timezone.now()).strftime(settings.DATETIME_FORMAT_END)

		url = self.__get_url(start = start, end = end)
		sign = self.__get_sign(start = start, end = end)
		headers = self.__get_authorization_header(sign)

		response = requests.get(url, headers = headers)
		content = response.content

		if response.ok:
			return json.loads(content)['stats']

		raise ServiceResultError(response.status_code, content)

	def __get_common_stat(self, **kwargs):
		"""
		Get common stat from zadarma
		:return:
		"""
		self.__method = settings.PBX['urls']['common_stat']
		stat = self.__get_stat(**kwargs)
		return stat

	def __get_pbx_stat(self, **kwargs):
		"""
		Get pbx stat from zadarma
		:param kwargs:
		:return:
		"""
		self.__method = settings.PBX['urls']['pbx_stat']
		stat = self.__get_stat(**kwargs)
		return stat

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

	def get_stat(self, params = StatParams(None, None, 0, '')):
		"""
		Update statistic
		:return:
		"""
		if not params.start:
			params.start = timezone.now()
		if not params.end:
			params.end = timezone.now()

		common_stat = self.__get_common_stat(start = params.start, end = params.end)
		pbx_stat = self.__get_pbx_stat(start = params.start, end = params.end)
		return {}
