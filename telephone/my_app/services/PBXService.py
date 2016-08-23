# coding=utf-8
import email
import hashlib
import hmac
import imaplib
import json
import urllib
from collections import OrderedDict, namedtuple

import requests
from datetime import datetime

from django.db.models import Q
from django.template import Context
from django.template.loader import get_template
from django.utils import timezone

from telephone import settings
from telephone.libs.File import File
from telephone.my_app.models import PBXCall, CallType, Caller, CallStatus
from telephone.my_app.services.ServiceBase import ServiceBase, ServiceResultError
from telephone.my_app.services.YandexDiskService import YandexDiskService
from telephone.my_app.utils import DateTimeUtil


class CountryCallsPriceList:
	def __init__(self, rows):
		self.__country = rows[0]['country']
		self.__rows = rows

	@property
	def country(self):
		"""
		Getter of __country
		:return: country value
		"""
		return self.__country

	@property
	def length(self):
		"""
		Getter of __length
		:return: length value
		"""
		return len(self.__rows)

	@property
	def price_list(self):
		"""
		Getter of __pricelist
		:return: pricelist value
		"""
		return [{'operator': r['country'], 'cost': r['cost_5']} for r in self.__rows]


StatParams = namedtuple('StatParams', ['start', 'end', 'status', 'call_type'])


class CallStatusQuery:
	def __init__(self, call_status):
		self.__status = int(call_status)

	@property
	def query(self):
		"""
		Getter of __query
		:return: query value
		"""
		if self.__status == 0:
			return Q()
		if self.__status == 1:
			return ~Q(status__name = 'answered')
		if self.__status == 2:
			return Q(status__name = 'answered')


class CallTypeQuery:
	def __init__(self, call_type):
		self.__type = call_type or 'incoming internal outgoing'

	@property
	def query(self):
		"""
		Getter of __query
		:return: query value
		"""
		return reduce(lambda q, x: q | Q(type__name = x), self.__type.split(' '), Q())


class Call:
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

		self.is_first_call = False

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
	_ResponseError = namedtuple('ResponseError', ['status', 'message'])

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

	def __find_in_pbx_typed(self, common_call, pbx_typed, with_seconds = True):
		"""
		Find suitable call in pbx_typed by date
		:param common_call:
		:param pbx_typed:
		:return:
		"""
		calls = filter(lambda x: DateTimeUtil.equals(x.date, common_call.date, with_seconds), pbx_typed)
		if len(calls) == 1:
			return calls[0]

		return None

	def __merge_calls(self, common_stat_list, stat_pbx_typed):
		"""
		Merge calls
		:param common_stat_list:
		:param stat_pbx_typed:
		:return:
		"""
		merged = []

		# Находим строку вида АТС - Номер А
		pbx_caller_calls = filter(lambda x: str(x.caller) == self.__pbx.phone_number and not PBXService.is_number_known(self.__pbx, x.to), common_stat_list.calls)
		# начинаем проверку не является ли она калбеком
		for pcc in pbx_caller_calls:

			call = Call()

			# Если ей нет соответствия во второй таблице, значит двустрочный калбек
			# Второй вид двустрочного калбека, это у которого вторая строка имеет вид Номер А - Номер Б
			second_row = filter(
				lambda x: str(x.caller) == str(pcc.to) and DateTimeUtil.equals(x.date, pcc.callstart, False), common_stat_list.calls)

			if len(second_row) == 1:
				# страка может иметь соответствующий входящий во второй таблице, может не иметь.
				# Если имеет, то записи должны упоминатся номера  А и Б
				second_row = second_row[0]
				pbx_call = self.__find_in_pbx_typed(second_row, filter(lambda x: x.call_type == 'incoming', stat_pbx_typed), False)
				if pbx_call:
					call = pbx_call
					call.clid = second_row.destination
					call.destination = pbx_call.clid
					call.description = pcc.description
					call.bill_seconds = pcc.bill_seconds
					call.cost = pcc.cost + second_row.cost
					call.bill_cost = pcc.bill_cost + second_row.bill_cost
					call.currency = pcc.currency
					call.sip = second_row.destination
					call.disposition = pcc.disposition
					pbx_call.merged = True
				else:
					call.call_id = pcc.call_id
					call.clid = pcc.sip
					call.sip = second_row.destination
					call.date = pcc.callstart
					call.destination = pcc.to
					call.disposition = pcc.disposition

					call.description = pcc.description
					call.bill_seconds = pcc.bill_seconds
					call.cost = pcc.cost + second_row.cost
					call.bill_cost = pcc.bill_cost + second_row.bill_cost
					call.currency = pcc.currency
				call.call_type = CallsConstants.COMING
				call.is_callback = True
				pcc.merged = True
				second_row.merged = True
				merged.append(call)
				continue

			# При первом варианте: двустрочный калбек. Он бывает двух видов в котором вторая строка(фактически она первая)
			# имеет вид АТС - Номер Б, находим её.
			second_row = filter(lambda x: str(x.caller) == str(self.__pbx.phone_number) and DateTimeUtil.equals(x.date, pcc.callstart, False) and not str(x.destination) == str(pcc.to), common_stat_list.calls)

			if len(second_row) == 1:
				# Ей должна соответствовать запись о входящем звонке в которой содержится номер А.
				# Если это так - значит всё это колбек(исходящий)
				second_row = second_row[0]
				pbx_call = self.__find_in_pbx_typed(second_row, filter(lambda x: x.call_type == 'incoming', stat_pbx_typed), False)
				if pbx_call:
					call = pbx_call
					call.call_type = CallsConstants.COMING
					call.sip = second_row.destination
					call.destination = pcc.to
					call.description = pcc.description
					call.bill_seconds = pcc.bill_seconds
					call.cost = pcc.cost + second_row.cost
					call.bill_cost = pcc.bill_cost + second_row.bill_cost
					call.currency = pcc.currency
					call.disposition = pcc.disposition
					call.is_callback = True
					merged.append(call)
					pcc.merged = True
					pbx_call.merged = True
					continue

			# искаем однострочный
			pbx_call = self.__find_in_pbx_typed(pcc, filter(lambda x: x.call_type == 'coming', stat_pbx_typed))
			if pbx_call:
				# Если соответствие есть - и это исходящий, значит это не калбек, а обычный исходящий звонок.
				call = pbx_call
				call.call_type = CallsConstants.COMING
				call.disposition = pcc.disposition
				call.description = pcc.description
				call.bill_seconds = pcc.bill_seconds
				call.cost = pcc.cost
				call.bill_cost = pcc.bill_cost
				call.currency = pcc.currency
				merged.append(call)
				pcc.merged = True
				pbx_call.merged = True
				continue

			pbx_call = self.__find_in_pbx_typed(pcc, filter(lambda x: x.call_type == 'incoming', stat_pbx_typed), False)
			if pbx_call:
				# Если соответствие есть, это входящий. значит однострочный калбек.
				call = pbx_call
				call.call_type = CallsConstants.COMING
				call.disposition = pcc.disposition
				call.destination = pcc.to
				call.sip = pbx_call.destination
				call.clid = pbx_call.destination
				call.description = pcc.description
				call.bill_seconds = pcc.bill_seconds
				call.cost = pcc.cost
				call.bill_cost = pcc.bill_cost
				call.currency = pcc.currency
				call.is_callback = True
				merged.append(call)
				pcc.merged = True
				pbx_call.merged = True
				continue

		return merged

	def __parse_other_calls(self, common_stat_list, stat_pbx_typed):
		"""
		Parse other calls
		:param stat_pbx_typed:
		:return:
		"""
		parsed = []

		for spt in stat_pbx_typed:

			call = Call()

			call_common = filter(lambda x: DateTimeUtil.equals(x.callstart, spt.date, True), common_stat_list.calls)

			if len(call_common) > 0:
				call_common = call_common[0]
				call = spt
				call.description = call_common.description,
				call.bill_seconds = call_common.billseconds,
				call.cost = call_common.cost,
				call.bill_cost = call_common.billcost,
				call.currency = call_common.currency
				parsed.append(call)
				# call_common.merged = True
				spt.merged = True
			else:
				if len(str(spt.sip)) == 3 and len(str(spt.destination)) == 3:
					spt.call_type = CallsConstants.INTERNAL
				call = spt
				spt.merged = True
				parsed.append(call)

		return parsed

	def __update_calls_list_by_type(self, stat, *args):
		"""
		Update calls table of each call type
		:param stat: existing stat
		:param args: calls lists
		:return:
		"""
		# message = '{row_to_update} row(s) to be inserted. '
		UpdateError = namedtuple('UpdateError', ['call', 'error'])
		update_errors = []
		total_rows_to_update = 0

		for arg in args:
			if len(arg) != 0:
				call_type = arg[0].call_type
				user_stat = stat.filter(type__name = call_type)

				row_to_update = len(arg) - len(user_stat)
				if row_to_update > 0:
					total_rows_to_update += row_to_update

					call_type_instance = CallType.objects.get_or_create(name = call_type)[0]
					for a in arg:
						# check if current call already exist
						stat_record = stat.filter(call_id = a.call_id)

						# save to db if not
						if not stat_record:
							caller = Caller.objects.create_caller(a.sip, self.__pbx.guid, a.date, a.description)
							call_status = CallStatus.objects.get_or_create(name = a.disposition)[0]
							try:
								call = PBXCall.objects.create_call(a, caller.guid, self.__pbx.guid, call_type_instance.guid, call_status.guid)
							except Exception as e:
								update_errors.append(UpdateError(a, e))

		if len(update_errors) > 0:
			# Update calls list succeed with errors
			pass

		return {}

	def __get_audio_from_mailbox(self, call_id):
		"""
		Check user mailbox to find the record
		:param call_id: id of the call
		:param user: current logged user
		:return: filename
		"""
		username = self.__pbx.user.yandexprofile.yandex_email
		password = self.__pbx.user.yandexprofile.yandex_password
		imap_server = 'imap.yandex.ru'
		header_start = 'audio/wav; name="'
		call_audio = None

		try:
			# connect to mailbox
			mailbox = imaplib.IMAP4_SSL(imap_server)
			mailbox.login(username, password)
			mailbox.select('INBOX')

			for msg_id in range(len(mailbox.search(None, 'ALL')[1][0].split()), 0, -1):
				message = email.message_from_string(mailbox.fetch(msg_id, '(RFC822)')[1][0][1])
				parts = message.get_payload()
				if isinstance(parts, list):
					for part in message.get_payload():
						if isinstance(part, email.message.Message):
							header = filter(lambda x: x.startswith(header_start) and x.find(call_id) > 0, part.values())
							if header and len(header) > 0:
								filename = header[0].strip(header_start)
								call_audio = File(part.get_payload(decode = True), filename)
								break
					if call_audio:
						break
			mailbox.logout()
		except Exception as e:
			pass

		return call_audio

	def __load_call_record_file(self, call):
		"""
		Load audio, convert, upload to disk and update db with filename
		:param call: Call instance
		:param user: current user
		:return: File instance
		"""
		# get audio
		call_audio = self.__get_audio_from_mailbox(call.call_id)
		if not call_audio:
			return None
		#
		# # convert audio
		# # write temp file
		# path = CommonService.write_temp_file(call_audio)
		# if not path:
		# 	return None
		#
		# call_audio.path = path
		#
		# # convert wav to mp3
		#
		# call_audio_mp3 = CommonService.convert_to_mp3(call_audio)
		# if not call_audio_mp3:
		# 	return None
		call_audio_mp3 = call_audio

		# upload new file to Disk
		disk_service = YandexDiskService(self.__pbx.user.yandexprofile)
		disk_service.upload(call_audio_mp3)

		filename = call_audio_mp3.filename
		# delete mp3 file form filesystem and save to db
		# CommonService.delete_temp_file(filename)

		call.record_filename = filename
		call.save()

		return call_audio_mp3

	def __get_call_record_file_dwn_link(self, call):
		"""
		Get call record download link by call
		:param call:
		:return:
		"""
		filename = call.record_filename
		if not filename:
			record_file = self.__load_call_record_file(call)
			filename = record_file.filename

		disk_service = YandexDiskService(self.__pbx.user.yandexprofile)
		link = disk_service.get_download_link(filename)
		return link

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

	def update_stat(self, params = StatParams(None, None, 0, '')):
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
		merged_calls = self.__merge_calls(common_stat_list, parsed_calls)
		other_calls = self.__parse_other_calls(common_stat_list, parsed_calls)

		calls = merged_calls + other_calls
		existing_calls = self.__pbx.pbxcall_set.filter(date__gte=params.start, date__lte=params.end)

		self.__update_calls_list_by_type(
			existing_calls,
			filter(lambda x: x.call_type == 'incoming', calls),
			filter(lambda x: x.call_type == 'coming', calls),
			filter(lambda x: x.call_type == 'internal', calls),
		)

	def get_call_cost(self, number):
		"""
		Get call cost
		:param number:
		:return:
		"""
		self.__method = settings.PBX['urls']['call_cost']

		url = self.__get_url(number = number)
		sign = self.__get_sign(number = number)
		headers = self.__get_authorization_header(sign)

		response = requests.get(url, headers = headers)
		content = json.loads(response.content)

		if response.ok:
			return content['info']

		raise ServiceResultError(response.status_code, self._ResponseError(**content))

	def get_call_record_file(self, call):
		"""
		Gets call's record file
		"""
		link = self.__get_call_record_file_dwn_link(call)

		disk_service = YandexDiskService(self.__pbx.user.yandexprofile)
		return disk_service.download(link)

	def get_costs_by_country(self, country):
		"""
		Get costs list by country
		:param country:
		:return:
		"""
		country = country.lower()
		response = requests.post(
			'https://zadarma.com/ru/checks/call-cost/',
			{'number': country},
			headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Cookie': 'currency=RUB; lang=en;'}
		)

		if response.ok:
			data = json.loads(response.content)
			rows = data['data'][0]['rows']
			return CountryCallsPriceList(rows)

		raise ServiceResultError(response.status_code)

	def generate_widget_script(self, counter_number):
		"""
		Generates ws
		:param counter_number:
		:return:
		"""
		ws = self.__pbx.get_widget_script()

		template = get_template(settings.WS_SCRIPT_TEMPLATE_NAME)
		ctx = Context({'widget_guid': ws.guid, 'counter_number': counter_number})
		return template.render(ctx)
