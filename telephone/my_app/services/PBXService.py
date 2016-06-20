# coding=utf-8
import hashlib
import hmac
import json
import urllib
from collections import OrderedDict, namedtuple

import requests
from datetime import datetime
from django.utils import timezone

from telephone import settings
from telephone.my_app.services.ServiceBase import ServiceBase, ServiceResultError
from telephone.my_app.utils import DateTimeUtil


StatParams = namedtuple('StatParams', ['start', 'end', 'status', 'call_type'])


class Call():
	def __init__(self):
		self.call_id = None
		self.clid = None
		self.sip = None
		self.date = None
		self.destination = None
		self.disposition = None
		# stat
		self.description = None
		self.bill_seconds = None
		self.cost = None
		self.bill_cost = None
		self.currency = None

		self.call_type = None
		self.is_callback = False

		self.__is_first_call = False

		self.merged = False


class CallsConstants:
	def __init__(self):
		pass

	ANSWERED = 'answered'
	INCOMING = 'incoming'
	COMING = 'coming'
	INTERNAL = 'internal'
	CALLBACK = 'callback'

	FAIL_TYPES = ['busy', 'cancel', 'no answer', 'failed', 'no money', 'unallocated number', 'no limit', 'no day limit', 'line limit', 'no money, no limit']


class CallList(object):
	"""
	Base CallList class
	"""
	def __init__(self):
		self._calls = []

	@property
	def calls(self):
		"""
		Getter of __calls
		:return: calls value
		"""
		return self._calls

	@property
	def count(self):
		"""
		Getter of count
		:return: count value
		"""
		return len(self._calls)

	def add(self, **kwargs):
		"""
		Add a call
		:return:
		"""
		raise NotImplementedError()


class CommonCallList(CallList):
	CommonCall = namedtuple('CommonCall', ['id', 'sip', 'callstart', 'caller', 'to', 'description', 'disposition', 'billseconds', 'cost', 'billcost', 'currency'])

	def add(self, **kwargs):
		"""
		Overrides base class method
		:return:
		"""
		kwargs['caller'] = kwargs['from']
		del kwargs['from']
		kwargs['callstart'] = datetime.strptime(kwargs['callstart'], settings.DATETIME_FORMAT_ALTER)
		call = self.CommonCall(**kwargs)
		self._calls.append(call)


class PBXCallList(CallList):
	PBXCall = namedtuple('PBXCall', ['call_id', 'sip', 'callstart', 'destination', 'disposition', 'seconds', 'clid', 'is_recorded'])

	def add(self, **kwargs):
		"""
		Overrides base class method
		:return:
		"""
		kwargs['callstart'] = datetime.strptime(kwargs['callstart'], settings.DATETIME_FORMAT_ALTER)
		call = self.PBXCall(**kwargs)
		self._calls.append(call)

	def group(self):
		"""
		Filter stat_pbx calls
		:param stat_pbx: List of calls
		:return: List of filtered calls
		"""
		result = []
		key_date_val = None
		key_sip_val = None
		group = []
		for call in self._calls:
			if not key_date_val:
				# init key_date_val
				key_date_val = call.callstart
			if not key_sip_val:
				# init key_sip_val
				key_sip_val = call.sip
			if (call.sip == key_sip_val and DateTimeUtil.equals(key_date_val, call.callstart, True)) or not group:
				# add to group if values are equals
				group.append(call)
			else:
				result.append(group)
				# set current call as the first group item
				group = [call]
				# update key values
				key_date_val = call.callstart
				key_sip_val = call.sip
			if call == self._calls[-1] and group:
				# add last group
				result.append(group)
		return result


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
		stats = self.__get_stat(**kwargs)

		calls_list = CommonCallList()
		for call in stats:
			calls_list.add(**call)

		return calls_list

	def __get_pbx_stat(self, **kwargs):
		"""
		Get pbx stat from zadarma
		:param kwargs:
		:return:
		"""
		self.__method = settings.PBX['urls']['pbx_stat']
		stats = self.__get_stat(**kwargs)

		calls_list = PBXCallList()
		for call in stats:
			calls_list.add(**call)

		return calls_list

	def __parse_calls(self, pbx_stat_list):
		"""
		Parse pbx_stat_list to incoming, outgoing, internal calls
		:param pbx_stat_list:
		:return:
		"""
		coming = []
		incoming = []
		internal = []

		pbx_stat_grouped = pbx_stat_list.group()

		for pbx_stat_group in pbx_stat_grouped:

			call = Call()
			pbx_incoming = filter(lambda x: x.destination == CallsConstants.INCOMING, pbx_stat_group)
			if len(pbx_incoming) is not 0:
				pbx_incoming_call = pbx_incoming[0]

				if pbx_incoming_call.disposition not in CallsConstants.FAIL_TYPES:
					pbx_call_same_disp = filter(lambda x: x.disposition == pbx_incoming_call.disposition and not x.destination == CallsConstants.INCOMING, pbx_stat_group)[0]
				else:
					pbx_call_same_disp = filter(lambda x: not x.destination == CallsConstants.INCOMING, pbx_stat_group)
					pbx_call_same_disp = pbx_stat_group[0] if len(pbx_call_same_disp) == 0 else pbx_call_same_disp[0]
				# TODO: parse clid
				call.call_id = pbx_call_same_disp.call_id
				call.clid = pbx_call_same_disp.clid
				call.sip = pbx_call_same_disp.sip
				call.date = pbx_call_same_disp.callstart
				call.destination = pbx_call_same_disp.destination
				call.disposition = pbx_incoming_call.disposition
				call.bill_seconds = pbx_incoming_call.seconds

			else:
				pbx_call = pbx_stat_group[0]
				call.call_id = pbx_call.call_id
				call.clid = pbx_call.clid
				call.sip = pbx_call.sip
				call.date = pbx_call.callstart
				call.destination = pbx_call.destination
				call.disposition = pbx_call.disposition
				call.bill_seconds = pbx_call.seconds

			if PBXService.is_number_known(self.__pbx, call.clid):
				# звонок исходящий либо внутренний

				if PBXService.is_number_known(self.__pbx, call.destination):
					# номер известный - звонок внутренний
					call.call_type = CallsConstants.INTERNAL
					if call.disposition in CallsConstants.FAIL_TYPES:
						call.destination = ''
					internal.append(call)
				else:
					# звонок исходящий
					call.call_type = CallsConstants.COMING
					if call.disposition in CallsConstants.FAIL_TYPES:
						call.destination = ''
					coming.append(call)
			else:
				# звонок входящий
				call.call_type = CallsConstants.INCOMING
				if call.disposition in CallsConstants.FAIL_TYPES:
					call.destination = ''
				incoming.append(call)

		return coming + incoming + internal

	@staticmethod
	def is_number_known(pbx, number):
		"""
		Check if the number is known
		:param number:
		:return:
		"""
		number = str(number)
		return len(pbx.redirectnumber_set.filter(number=number)) > 0 or 'Internal' in number or len(number) == 3 or 'w00e' in number

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

		common_stat_list = self.__get_common_stat(start = params.start, end = params.end)
		pbx_stat_list = self.__get_pbx_stat(start = params.start, end = params.end)

		parsed_calls = self.__parse_calls(pbx_stat_list)
		return {}
