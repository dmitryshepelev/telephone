# coding=utf-8
import email
import imaplib
import json

import requests

from telephone import settings
from telephone.classes.ApiParams import ApiParams
from telephone.classes.Call import Call, CallRecord, CallPBX
from telephone.classes.File import File
from telephone.classes.ServiceResponse import ServiceResponse
from telephone.main_app.models import RedirectNumbers, RegisteredCallback
from telephone.service_app.services.CommonService import CommonService, CallsConstants
from telephone.service_app.services.DBService import DBService
from telephone.service_app.services.DiskService import DiskService
from telephone.service_app.services.LogService import Code, LogService


class PBXDataService():
	def __init__(self):
		pass

	@staticmethod
	def get_common_stat(params, user):
		"""
		Get statistics from api
		:param params: ApiParameters instance
		:param user: User instance
		:return: json type
		"""
		method = settings.API_URLS['api']['common_stat']
		api_response = requests.get(params.get_request_string(method), headers={'Authorization': '%s:%s' % (user.userprofile.user_key, CommonService.get_sign(params, method, params.api_version, user.userprofile.secret_key))})
		if api_response.ok:
			return ServiceResponse(api_response.ok, [Call(s) for s in json.loads(api_response.content)['stats']])
		return ServiceResponse(api_response.ok, status_code=api_response.status_code)

	@staticmethod
	def get_pbx_stat(params, user):
		"""
		Get ats statistics from api
		:param params: CallParameters instance
		:param user: User instance
		:return: json type
		"""
		method = settings.API_URLS['api']['pbx_stat']

		api_response = requests.get(params.get_request_string(method), headers={'Authorization': '%s:%s' % (user.userprofile.user_key, CommonService.get_sign(params, method, params.api_version, user.userprofile.secret_key))})
		if api_response.ok:
			return ServiceResponse(api_response.ok, [CallPBX(s) for s in json.loads(api_response.content)['stats']])
		return ServiceResponse(api_response.ok, status_code=api_response.status_code)

	@staticmethod
	def reduce_grouped(grouped, groups):
		"""
		Remove groups from the grouped
		:param grouped:
		:param groups:
		"""
		for group in groups:
			grouped.remove(group)

	@staticmethod
	def group_stat_pbx(stat_pbx):
		"""
		Filter stat_pbx calls
		:param stat_pbx: List of calls
		:return: List of filtered calls
		"""
		result = []
		key_date_val = None
		key_sip_val = None
		group = []
		for s in stat_pbx:
			if not key_date_val:
				# init key_date_val
				key_date_val = s.date
			if not key_sip_val:
				# init key_sip_val
				key_sip_val = s.sip
			if (s.sip == key_sip_val and CommonService.is_dates_equals(key_date_val, s.date, True)) or not group:
				# add to group if values are equals
				group.append(s)
			else:
				result.append(group)
				# set current call as the first group item
				group = [s]
				# update key values
				key_date_val = s.date
				key_sip_val = s.sip
			if s == stat_pbx[-1] and group:
				# add last group
				result.append(group)
		return result

	@staticmethod
	def is_number_known(number, userprofile):
		number = str(number)
		return len(userprofile.redirectnumbers_set.filter(number=number)) > 0\
		       or 'Internal' in number\
		       or len(str(number)) == 3\
		       or 'w00e' in str(number)

	@staticmethod
	def parse_calls(stat_common, stat_pbx_grouped, userprofile):
		coming = []
		incoming = []
		internal = []

		for stat_pbx_group in stat_pbx_grouped:

			call = CallRecord()
			pbx_incoming = filter(lambda x: x.destination == CallsConstants.INCOMING, stat_pbx_group)
			if len(pbx_incoming) is not 0:
				pbx_incoming_call = pbx_incoming[0]

				pbx_call_same_disp = None
				if not pbx_incoming_call.disposition in CallsConstants.FAIL_TYPES:
					pbx_call_same_disp = filter(lambda x: x.disposition == pbx_incoming_call.disposition and not x.destination == CallsConstants.INCOMING, stat_pbx_group)[0]
				else:
					pbx_call_same_disp = filter(lambda x: not x.destination == CallsConstants.INCOMING, stat_pbx_group)
					pbx_call_same_disp = stat_pbx_group[0] if len(pbx_call_same_disp) == 0 else pbx_call_same_disp[0]

				call.set_params(
					call_id=pbx_call_same_disp.call_id,
					clid=pbx_call_same_disp.clid,
					sip=pbx_call_same_disp.sip,
					date=pbx_call_same_disp.date,
					destination=pbx_call_same_disp.destination,
					disposition=pbx_incoming_call.disposition,
					bill_seconds=pbx_incoming_call.seconds
				)

			else:
				pbx_call = stat_pbx_group[0]
				call.set_params(
					call_id=pbx_call.call_id,
					clid=pbx_call.clid,
					sip=pbx_call.sip,
					date=pbx_call.date,
					destination=pbx_call.destination,
					disposition=pbx_call.disposition,
					bill_seconds=pbx_call.seconds
				)

			if PBXDataService.is_number_known(call.clid, userprofile):
				# звонок исходящий либо внутренний

				if PBXDataService.is_number_known(call.destination, userprofile):
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
	def find_in_pbx_typed(common_call, pbx_typed, with_seconds=True):
		"""
		Find suitable call in pbx_typed by date
		:param common_call:
		:param pbx_typed:
		:return:
		"""
		calls = filter(lambda x: CommonService.is_dates_equals(x.date, common_call.date, with_seconds), pbx_typed)
		if len(calls) == 1:
			return calls[0]

		return None

	@staticmethod
	def merge(stat_common, stat_pbx_typed, userprofile):

		merged = []

		# Находим строку вида АТС - Номер А
		pbx_caller_calls = filter(lambda x: str(x.caller) == userprofile.profile_phone_number
		                                    and not PBXDataService.is_number_known(x.destination, userprofile), stat_common)
		# начинаем проверку не является ли она калбеком
		for pcc in pbx_caller_calls:

			call = CallRecord()

			# Если ей нет соответствия во второй таблице, значит двустрочный калбек
			# Второй вид двустрочного калбека, это у которого вторая строка имеет вид Номер А - Номер Б
			second_row = filter(lambda x: str(x.caller) == str(pcc.destination) and CommonService.is_dates_equals(x.date, pcc.date, False), stat_common)

			if len(second_row) == 1:
				# страка может иметь соответствующий входящий во второй таблице, может не иметь.
				# Если имеет, то записи должны упоминатся номера  А и Б
				second_row = second_row[0]
				pbx_call = PBXDataService.find_in_pbx_typed(second_row, filter(lambda x: x.call_type == 'incoming', stat_pbx_typed), False)
				if pbx_call:
					call = pbx_call
					call.set_params(
						clid=second_row.destination,
						destination=pbx_call.clid,
						description=pcc.description,
						bill_seconds=pcc.bill_seconds,
						cost=pcc.cost + second_row.cost,
						bill_cost=pcc.bill_cost + second_row.bill_cost,
						currency=pcc.currency,
						sip=second_row.destination,
						disposition=pcc.disposition
					)
					pbx_call.merged = True
				else:
					call.set_params(
						call_id=pcc.call_id,
						clid=pcc.sip,
						sip=second_row.destination,
						date=pcc.date,
						destination=pcc.destination,
						disposition=pcc.disposition,

						description=pcc.description,
						bill_seconds=pcc.bill_seconds,
						cost=pcc.cost + second_row.cost,
						bill_cost=pcc.bill_cost + second_row.bill_cost,
						currency=pcc.currency
					)
				call.call_type = CallsConstants.COMING
				call.is_callback = True
				pcc.merged = True
				second_row.merged = True
				merged.append(call)
				continue

			# При первом варианте: двустрочный калбек. Он бывает двух видов в котором вторая строка(фактически она первая)
			# имеет вид АТС - Номер Б, находим её.
			second_row = filter(lambda x: str(x.caller) == str(userprofile.profile_phone_number)
			                              and CommonService.is_dates_equals(x.date, pcc.date, False)
			                              and not str(x.destination) == str(pcc.destination), stat_common)

			if len(second_row) == 1:
				# Ей должна соответствовать запись о входящем звонке в которой содержится номер А.
				# Если это так - значит всё это колбек(исходящий)
				second_row = second_row[0]
				pbx_call = PBXDataService.find_in_pbx_typed(second_row, filter(lambda x: x.call_type == 'incoming', stat_pbx_typed), False)
				if pbx_call:
					call = pbx_call
					call.call_type = CallsConstants.COMING
					call.set_params(
						sip=second_row.destination,
						destination=pcc.destination,
						description=pcc.description,
						bill_seconds=pcc.bill_seconds,
						cost=pcc.cost + second_row.cost,
						bill_cost=pcc.bill_cost + second_row.bill_cost,
						currency=pcc.currency,
						disposition=pcc.disposition
					)
					call.is_callback = True
					merged.append(call)
					pcc.merged = True
					pbx_call.merged = True
					continue

			# искаем однострочный
			pbx_call = PBXDataService.find_in_pbx_typed(pcc, filter(lambda x: x.call_type == 'coming', stat_pbx_typed))
			if pbx_call:
				# Если соответствие есть - и это исходящий, значит это не калбек, а обычный исходящий звонок.
				call = pbx_call
				call.call_type = CallsConstants.COMING
				call.set_params(
					disposition=pcc.disposition,
					description=pcc.description,
					bill_seconds=pcc.bill_seconds,
					cost=pcc.cost,
					bill_cost=pcc.bill_cost,
					currency=pcc.currency
				)
				merged.append(call)
				pcc.merged = True
				pbx_call.merged = True
				continue

			pbx_call = PBXDataService.find_in_pbx_typed(pcc, filter(lambda x: x.call_type == 'incoming', stat_pbx_typed), False)
			if pbx_call:
				# Если соответствие есть, это входящий. значит однострочный калбек.
				call = pbx_call
				call.call_type = CallsConstants.COMING
				call.set_params(
					disposition=pcc.disposition,
					destination=pcc.destination,
					sip=pbx_call.destination,
					clid=pbx_call.destination,
					description=pcc.description,
					bill_seconds=pcc.bill_seconds,
					cost=pcc.cost,
					bill_cost=pcc.bill_cost,
					currency=pcc.currency
				)
				call.is_callback = True
				merged.append(call)
				pcc.merged = True
				pbx_call.merged = True
				continue

		return merged

	@staticmethod
	def parse_other(stat_common, stat_pbx_typed, userprofile):

		parsed = []

		for spt in stat_pbx_typed:

			call = CallRecord()

			call_common = filter(lambda x: CommonService.is_dates_equals(x.date, spt.date, True), stat_common)

			if len(call_common) > 0:
				call_common = call_common[0]
				call = spt
				call.set_params(
					description=call_common.description,
					bill_seconds=call_common.bill_seconds,
					cost=call_common.cost,
					bill_cost=call_common.bill_cost,
					currency=call_common.currency
				)
				parsed.append(call)
				call_common.merged = True
				spt.merged = True
			else:
				if len(str(spt.sip)) == 3 and len(str(spt.destination)) == 3:
					spt.call_type = CallsConstants.INTERNAL
				call = spt
				spt.merged = True
				parsed.append(call)

		return parsed

	@staticmethod
	def update_calls_list(params, user):
		"""
		Update db table Calls
		:param params: ApiParams
		:param user: User
		:return:
		"""
		# get common stat
		stat_common_res = PBXDataService.get_common_stat(params, user)
		if not stat_common_res.is_success:
			return ServiceResponse(False, message=Code.UCLUNS, data={'params': params, 'user_id': user.pk}, status_code=stat_common_res.status_code)

		# get pbx stat
		stat_pbx_res = PBXDataService.get_pbx_stat(params, user)
		if not stat_pbx_res.is_success:
			return ServiceResponse(False, message=Code.UCLUNS, data={'params': params, 'user_id': user.pk}, status_code=stat_pbx_res.status_code)

		# group pbx stat
		stat_pbx_grouped = PBXDataService.group_stat_pbx(stat_pbx_res.data)

		parseed_calls = PBXDataService.parse_calls(stat_common_res.data, stat_pbx_grouped, user.userprofile)
		callbacks = PBXDataService.merge(stat_common_res.data, parseed_calls, user.userprofile)

		other_calls = PBXDataService.parse_other(
			filter(lambda x: not x.merged, stat_common_res.data),
			filter(lambda x: not x.merged, parseed_calls),
			user.userprofile
		)

		calls = callbacks + other_calls

		# Get existing calls stat
		user_stat = user.userprofile.call_set.filter(date__gte=params.start, date__lte=params.end)

		# update calls table and return
		return PBXDataService.update_calls_list_by_type(
			user.userprofile,
			user_stat,
			filter(lambda x: x.call_type == 'incoming', calls),
			filter(lambda x: x.call_type == 'coming', calls),
			filter(lambda x: x.call_type == 'internal', calls),
		)

	@staticmethod
	def update_calls_list_by_type(userprofile, stat, *args):
		"""
		Update calls table of each call type
		:param userprofile: user profile
		:param stat: existing stat
		:param args: calls lists
		:return:
		"""
		message = '{row_to_update} row(s) to be inserted. '
		update_errors = []
		total_rows_to_update = 0

		for arg in args:
			if len(arg) != 0:
				call_type = arg[0].call_type
				user_stat = stat.filter(call_type=call_type)

				row_to_update = len(arg) - len(user_stat)
				if row_to_update > 0:
					total_rows_to_update += row_to_update

					for a in arg:
						# check if current call already exist
						stat_record = stat.filter(call_id=a.call_id)

						# save to db if not
						if not stat_record:
							result = DBService.create_call(a, userprofile)

							if not result.is_success:
								update_errors.append((result.data, result.message,))

		if len(update_errors) > 0:
			# Update calls list succeed with errors
			message = message.format(row_to_update=total_rows_to_update)
			message += Code.UCLSWE

		return ServiceResponse(True, data=update_errors, message=message)

	@staticmethod
	def get_audio(call_id, user):
		"""
		Check user mailbox to find the record
		:param call_id: id of the call
		:param user: current logged user
		:return: filename
		"""
		username = user.userprofile.profile_email
		password = user.userprofile.profile_password
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
				for part in message.get_payload():
					if isinstance(part, email.message.Message):
						header = filter(lambda x: x.startswith(header_start) and x.find(call_id) > 0, part.values())
						if header and len(header) > 0:
							filename = header[0].strip(header_start)
							call_audio = File(part.get_payload(decode=True), filename + 'wav')
							break
				if call_audio:
					break
			mailbox.logout()
		except Exception as e:
			logger = LogService()
			logger.error(Code.GET_AUDIO_ERR, message=str(e), call_id=call_id, username=user.username)
			return None
		return call_audio

	@staticmethod
	def load_call_record_file(call, user):
		"""
		Load audio, convert, upload to disk and update db with filename
		:param call: Call instance
		:param user: current user
		:return: File instance
		"""
		# get audio
		call_audio = PBXDataService.get_audio(call.call_id, user)
		if not call_audio:
			return None

		# convert audio
		# write temp file
		path = CommonService.write_temp_file(call_audio)
		if not path:
			return None

		call_audio.path = path

		# convert wav to mp3

		call_audio_mp3 = CommonService.convert_to_mp3(call_audio)
		if not call_audio_mp3:
			return None

		# upload new file to Disk
		disk_service = DiskService(user.userprofile.token)
		result = disk_service.upload_file(call_audio_mp3)
		if not result.is_success:
			return None

		filename = call_audio_mp3.filename
		# delete mp3 file form filesystem and save to db
		CommonService.delete_temp_file(filename)

		try:
			call.record_filename = filename
			call.save()
		except Exception as e:
			logger = LogService()
			logger.error(Code.UPDATE_CALL_ERR, message=str(e), call_id=call.pk, filename=filename)
			return None

		return filename

	@staticmethod
	def get_call_record_filename(call_id, user):
		"""
		Get call record filename by call_id
		:param call_id: id of the call
		:param user: current user
		:return: {str} filename
		"""
		call = DBService.get_call(call_id=call_id)
		if not call:
			return None

		# check if current user is the master of the call
		if call.user_profile_id != user.userprofile.pk:
			return None

		# check if the record was already loaded
		filename = call.record_filename
		if not filename:
			# load new record
			filename = PBXDataService.load_call_record_file(call, user)
			if not filename:
				return None
		return filename

	@staticmethod
	def get_call_record_download_link(call_id, user):
		"""
		Get call record download link by call_id
		:param call_id: id of the call
		:param user: current user
		:return: call record download link
		"""
		filename = PBXDataService.get_call_record_filename(call_id, user)
		if not filename:
			return None

		# download file from disk
		disk_service = DiskService(user.userprofile.token)
		return disk_service.get_download_link(filename)

	@staticmethod
	def get_call_record_file(call_id, user):
		"""
		Get call record file by call_id
		:param call_id: id of the call
		:param user: current user
		:return: call record File instance
		"""
		link = PBXDataService.get_call_record_download_link(call_id, user)
		if not link:
			return None

		disk_service = DiskService(user.userprofile.token)
		return disk_service.download_file(link)

	@staticmethod
	def get_pbx_account_balance(user):
		"""
		Get current user account balance
		:param user: user instance
		:return: {float} current balance
		"""
		host = settings.API_URLS['api']['host']
		api_version = settings.API_URLS['api']['api_version']
		method = settings.API_URLS['api']['balance']

		url = '{host}{api_version}{method}'.format(host=host, api_version=api_version, method=method)

		response = requests.get(url, headers={'Authorization': '%s:%s' % (user.userprofile.user_key, CommonService.get_sign({}, method, api_version, user.userprofile.secret_key))})
		content = response.content

		if response.ok:
			return json.loads(content)['balance']

		logger = LogService()
		logger.error(Code.GET_BALANCE_ERR, data=json.loads(content), status_code=response.status_code)
		return None

	@staticmethod
	def get_call_cost(user, to):
		"""
		Get the cost of the call
		:param to: target phone number
		:return:
		"""
		method = settings.API_URLS['api']['call_cost']

		# WARNING: Creates ApiParams with {start} and {end} params. Needs to be refactored
		params = ApiParams({'number': to})
		url = params.get_request_string(method)

		response = requests.get(url, headers={'Authorization': '%s:%s' % (user.userprofile.user_key, CommonService.get_sign(params, method, params.api_version, user.userprofile.secret_key))})
		content = response.content

		if response.ok:
			return json.loads(content)['info']

		logger = LogService()
		logger.error(Code.GET_CALL_COST_ERR, data=json.loads(content), status_code=response.status_code)
		return None

	@staticmethod
	def request_callback(user, from_number, to_number):
		"""
		Request the callback
		:param user: user instance
		:param form: prom number
		:param to: to number
		:return:
		"""
		method = settings.API_URLS['api']['request_callback']

		# WARNING: Creates ApiParams with {start} and {end} params. Needs to be refactored
		params = ApiParams({'from': from_number, 'to': to_number})
		url = params.get_request_string(method)

		response = requests.get(url, headers={'Authorization': '%s:%s' % (user.userprofile.user_key, CommonService.get_sign(params, method, params.api_version, user.userprofile.secret_key))})
		content = response.content

		if response.ok:
			callback = DBService.register_callback(user.userprofile, from_number, to_number)
			if callback:
				return json.loads(content)

		logger = LogService()
		logger.error(Code.REQUEST_CALLBACK_ERR, data=json.loads(content), status_code=response.status_code)
		return None

	@staticmethod
	def get_pbx_sip(user):
		"""
		Get sip number
		:param user: user
		:return: sip
		"""
		method = settings.API_URLS['api']['sip']

		# WARNING: Creates ApiParams with {start} and {end} params. Needs to be refactored
		params = ApiParams()
		url = params.get_request_string(method)

		response = requests.get(url, headers={'Authorization': '%s:%s' % (user.userprofile.user_key, CommonService.get_sign(params, method, params.api_version, user.userprofile.secret_key))})
		content = response.content

		if response.ok:
			sips = json.loads(content)['sips']
			sip = int(filter(lambda s: s['display_name'] == 'SIP', sips)[0]['id'])
			return sip

		logger = LogService()
		logger.error(Code.SIP_GETTING_ERR, data=json.loads(content), status_code=response.status_code)
		return None