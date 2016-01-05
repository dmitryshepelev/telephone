import email
import imaplib
import json

import requests

from telephone import settings
from telephone.classes.ApiParams import ApiParams
from telephone.classes.Call import Call, CallRecord, CallPBX
from telephone.classes.File import File
from telephone.classes.ServiceResponse import ServiceResponse
from telephone.main_app.models import RedirectNumbers
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
	def get_coming_calls(stat_common, stat_pbx_grouped, user):
		"""
		Gets coming external calls.
		The coming external calls are represented by one record in both tables.
		For PBX table, the record's {clid} field contains 'Internal' text
		For STAT table, the {from} field contains profile phone number value
		The dates of both record are the same with
		:param stat_common: calls stat
		:param stat_pbx_grouped: grouped pbx stat
		:param user: user profile
		:return: Array of CallRecord instances
		"""
		result = []
		redirect_numbers = user.redirectnumbers_set

		for group in stat_pbx_grouped:
			if len(group) == 1 and 'Internal' in group[0].clid and len(redirect_numbers.filter(number=group[0].destination)) == 0:
				stat_common_record = filter(lambda x: x.caller == int(user.profile_phone_number)
													and CommonService.is_dates_equals(x.date, group[0].date, False)
													and x.destination == group[0].destination, stat_common)

				if len(stat_common_record) == 1:
					call = CallRecord()
					call.set_params(**group[0].__dict__)
					call.set_params(bill_cost=stat_common_record[0].bill_cost, bill_seconds=stat_common_record[0].bill_seconds, cost=stat_common_record[0].cost,
									currency=stat_common_record[0].currency, description=stat_common_record[0].description, call_type=CallsConstants.COMING)

					result.append(call)

		return result

	@staticmethod
	def get_internal_calls(stat_common, stat_pbx_grouped, user):
		"""
		Gets internal calls.
		The internal calls might be with or without redirection
		The calls without redirection are the only record in PBX table
			with {clid} field contained 'Internal' text, {destination} field is an internal number (100, 101, ect.)
			and {sip} is an internal caller number
		:param stat_common: calls stat
		:param stat_pbx_grouped: grouped pbx stat
		:param user: user profile
		:return: Array of CallRecord instances
		"""
		result = []
		redirect_numbers = user.redirectnumbers_set

		for group in stat_pbx_grouped:
			if len(group) == 1 and 'Internal' in group[0].clid:
				if len(str(group[0].destination)) == 3:
					# internal call without redirection
					call = CallRecord()
					call.set_params(**group[0].__dict__)
					call.bill_seconds = group[0].seconds
					call.call_type = CallsConstants.INTERNAL
					result.append(call)
				elif len(redirect_numbers.filter(number=group[0].destination)) == 1:
					# internal call with redirection
					stat_common_record = filter(lambda x: x.destination == group[0].destination
														and x.caller == int(user.profile_phone_number)
														and CommonService.is_dates_equals(x.date, group[0].date, False), stat_common)
					if len(stat_common_record) == 1:
						call = CallRecord()
						call.call_type = CallsConstants.INTERNAL
						call.set_params(**group[0].__dict__)
						call.set_params(bill_cost=stat_common_record[0].bill_cost, bill_seconds=stat_common_record[0].bill_seconds, cost=stat_common_record[0].cost,
										currency=stat_common_record[0].currency, description=stat_common_record[0].description, call_type=CallsConstants.INTERNAL)
						result.append(call)
		return result

	@staticmethod
	def get_other_calls(stat_common, stat_pbx_grouped, userprofile):
		"""
		Gets callback calls.
		The callback calls might be with or without redirection
		The calls without redirection are the three records in PBX table
			{clid} and {sip} fields contained target phone number, {destination} field is an internal number (100, 101, ect.)
		:param stat_common: calls stat
		:param stat_pbx_grouped: grouped pbx stat
		:param userprofile: user profile
		:return: Array of CallRecord instances
		"""
		result_coming = []
		result_incoming = []

		for group in stat_pbx_grouped:
			call = CallRecord()
			call.call_type = CallsConstants.COMING

			call_incoming_dest = filter(lambda x: x.destination == CallsConstants.INCOMING, group)
			if len(call_incoming_dest) == 1:
				call_answered_disp = filter(lambda x: x.disposition == call_incoming_dest[0].disposition and not x.destination == CallsConstants.INCOMING, group)
				if len(call_answered_disp) == 1:
					if len(str(call_answered_disp[0].destination)) == 3:
						# without redirection
						print(call_incoming_dest[0].date, 'first')
						call_common_record = filter(lambda x: str(x.caller) == userprofile.profile_phone_number
															and str(x.destination) == str(call_answered_disp[0].clid)
															and CommonService.is_dates_equals(x.date, call_answered_disp[0].date, False), stat_common)
						if len(call_common_record) == 1:
							call.set_params(
								call_id=call_answered_disp[0].call_id,
								clid=call_incoming_dest[0].clid,
								sip=call_answered_disp[0].destination,
								date=call_answered_disp[0].date,
								destination=call_common_record[0].destination,
								disposition=call_incoming_dest[0].disposition,
								description=call_common_record[0].description,
								bill_seconds=call_incoming_dest[0].seconds,
								cost=call_common_record[0].cost,
								bill_cost=call_common_record[0].bill_cost,
								currency=call_common_record[0].currency
							)
							result_coming.append(call)

					elif str(call_answered_disp[0].destination) in [rn.number for rn in RedirectNumbers.objects.filter(user_profile_id=userprofile.pk)]:
						# with redirection
						print(call_incoming_dest[0].date, 'second')
						call_common_record_1 = filter(lambda x: str(x.caller) == str(call_answered_disp[0].clid)
									and str(x.destination) == str(call_answered_disp[0].destination)
									and CommonService.is_dates_equals(x.date, call_answered_disp[0].date, False), stat_common)

						call_common_record_2 = filter(lambda x: str(x.caller) == userprofile.profile_phone_number
									and str(x.destination) == str(call_answered_disp[0].clid)
									and CommonService.is_dates_equals(x.date, call_answered_disp[0].date, False), stat_common)

						is_coming = True
						if len(call_common_record_2) == 0:
							call.call_type = CallsConstants.INCOMING
							is_coming = False

						if len(call_common_record_1) == 1:
							call.set_params(
								call_id=call_answered_disp[0].call_id,
								clid=call_incoming_dest[0].clid,
								sip=(call_common_record_1[0].destination if is_coming else call_common_record_1[0].caller),
								date=call_answered_disp[0].date,
								destination=(call_common_record_1[0].caller if is_coming else call_common_record_1[0].destination),
								disposition=call_incoming_dest[0].disposition,
								description=call_common_record_1[0].description,
								bill_seconds=call_incoming_dest[0].seconds,
								cost=call_common_record_1[0].cost,
								bill_cost=call_common_record_1[0].bill_cost,
								currency=call_common_record_1[0].currency
							)
							if is_coming:
								result_coming.append(call)
							else:
								result_incoming.append(call)

					else:
						print(call_incoming_dest[0].date, 'third')
					# call.call_type = CallsConstants.CALLBACK
					# call.set_params(call_id=group[0].call_id, sip=group[0].sip, clid=group[0].clid, date=group[0].date,
					# 				destination=stat_common_record[0].destination, disposition=stat_common_record[0].disposition,
					# 				description=stat_common_record[0].description, bill_cost=stat_common_record[0].bill_cost,
					# 				bill_seconds=stat_common_record[0].bill_seconds, cost=stat_common_record[0].cost,
					# 				currency=stat_common_record[0].currency)
					# result.append(call)
		return [result_coming, result_incoming]

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

		coming_calls = PBXDataService.get_coming_calls(stat_common_res.data, stat_pbx_grouped, user.userprofile)
		internal_calls = PBXDataService.get_internal_calls(stat_common_res.data, stat_pbx_grouped, user.userprofile)
		other_calls = PBXDataService.get_other_calls(stat_common_res.data, stat_pbx_grouped, user.userprofile)

		# Get existing calls stat
		user_stat = user.userprofile.call_set.filter(date__gte=params.start, date__lte=params.end)

		# update calls table and return
		return PBXDataService.update_calls_list_by_type(user.userprofile, user_stat, coming_calls, internal_calls, other_calls[0], other_calls[1])

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
						print(part)
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