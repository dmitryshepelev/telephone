import email
import imaplib
import json

import requests
from pydub import AudioSegment

from telephone import settings
from telephone.classes.Call import Call, CallRecord, CallPBX
from telephone.classes.File import File
from telephone.classes.ServiceResponse import ServiceResponse
from telephone.service_app.services.CommonService import CommonService, CallsConstants
from telephone.service_app.services.DBService import DBService
from telephone.service_app.services.DiskService import DiskService
from telephone.service_app.services.LogService import Code


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

		if settings.TEST_MODE or user.is_superuser:
			abspath = open(settings.BASE_DIR + '/static/content/stat.csv', 'r')
			data_arr = CommonService.parse_csv(abspath.read())
			return ServiceResponse(True, [Call(d) for d in data_arr])

		api_response = requests.get(params.get_request_string(method), headers={'Authorization': '%s:%s' % (user.userprofile.user_key, params.get_sign(method, user.userprofile.secret_key))})
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

		api_response = requests.get(params.get_request_string(method), headers={'Authorization': '%s:%s' % (user.userprofile.user_key, params.get_sign(method, user.userprofile.secret_key))})
		if api_response.ok:
			return ServiceResponse(api_response.ok, [CallPBX(s) for s in json.loads(api_response.content)['stats']])
		return ServiceResponse(api_response.ok, status_code=api_response.status_code)

	@staticmethod
	def filter_group(group):
		"""
		Filter the group of the calls
		:param group: stat_pbx group
		:return: CallRecord
		"""
		# filter answered calls form group
		answ_calls = [g for g in group if g.disposition == CallsConstants.ANSWERED]

		call = CallRecord()

		# check if call wasn't answered
		if not answ_calls:
			# ser params with 'destination' = None
			call.set_params(call_id=group[0].call_id, clid=group[0].clid, date=group[0].date, disposition=group[0].disposition, bill_seconds=group[0].seconds, sip=group[0].sip)
			call.is_answered = False
			return call

		# find incoming call
		for c in answ_calls:
			if c.destination == CallsConstants.INCOMING:
				call.set_params(bill_seconds=c.seconds)
			else:
				call.set_params(call_id=c.call_id, clid=c.clid, date=c.date, destination=c.destination, disposition=c.disposition, sip=c.sip)
		return call

	@staticmethod
	def filter_stat_pbx(stat_pbx):
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
			if CommonService.is_dates_equals(key_date_val, s.date, True and s.sip == key_sip_val) or not group:
				# add to group if values are equals
				group.append(s)
			else:
				result.append(PBXDataService.filter_group(group))
				# set current call as the first group item
				group = [s]
				# update key values
				key_date_val = s.date
				key_sip_val = s.sip
			if s == stat_pbx[-1] and group:
				# add last group
				result.append(PBXDataService.filter_group(group))
		return result


	@staticmethod
	def merge_calls(stat_common, stat_pbx):
		"""
		Merge statistic
		:param stat_common: calls statistic
		:param stat_pbx: PBX calls statistic
		:return: ServiceResponse
		"""
		result = []
		stat_pbx_filtered = PBXDataService.filter_stat_pbx(stat_pbx)
		for s in stat_pbx_filtered:
			stat_common_filtered = filter(lambda x: abs(x.bill_seconds - s.bill_seconds) <= 1 and
													(x.destination == s.destination if s.destination else CommonService.is_dates_equals(x.date, s.date, False) and
													 CommonService.is_dates_equals(x.date, s.date, False)), stat_common)
			if stat_common_filtered:
				s.set_params(bill_cost=stat_common_filtered[0].bill_cost, cost=stat_common_filtered[0].cost, currency=stat_common_filtered[0].currency, description=stat_common_filtered[0].description)
				result.append(s)
		return result

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

		merged_stat = PBXDataService.merge_calls(stat_common_res.data, stat_pbx_res.data)
		user_stat = user.userprofile.call_set.filter(date__gte=params.start, date__lte=params.end)

		# count of the rows need to be updated
		row_to_update = len(merged_stat) - len(user_stat)
		message = '{row_to_update} row(s) to be updated. '.format(row_to_update=row_to_update)
		update_errors = []
		if row_to_update > 0:
			for m_s in merged_stat:
				# check if current call already exist
				stat_record = user_stat.filter(call_id=m_s.call_id)
				# save to db if not
				if not stat_record:
					result = DBService.create_call(m_s, user.userprofile)
					if not result.is_success:
						update_errors.append((result.data, result.message,))
			if update_errors:
				# Update calls list succeed with errors
				message += Code.UCLSWE
		else:
			# Nothing to update
			message = Code.UCLNTU
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
			mailbox = imaplib.IMAP4_SSL(imap_server)
			mailbox.login(username, password)
			mailbox.select('INBOX')

			for msg_id in range(len(mailbox.search(None, 'ALL')[1][0].split()), 0, -1):
				message = email.message_from_string(mailbox.fetch(msg_id, '(RFC822)')[1][0][1])
				for part in message.get_payload():
					header = filter(lambda x: x.startswith(header_start) and x.find(call_id) > 0, part.values())
					if header and len(header) > 0:
						filename = header[0].strip(header_start)
						call_audio = File(part.get_payload(decode=True), filename + 'wav')
						break
				if call_audio:
					break
			mailbox.logout()
		except Exception as e:
			return ServiceResponse(False, message=e.message)
		return ServiceResponse(True, data=call_audio)

	@staticmethod
	def load_call_record_file(call, user):
		"""
		Load audio, convert, upload to disk and update db with filename
		:param call: Call instance
		:param user: current user
		:return: ServiceResponse
		"""
		# get audio
		result = PBXDataService.get_audio(call.call_id, user)
		if result.is_success:
			call_audio = result.data
			# convert audio
			result = CommonService.write_temp_file(call_audio)
			if result.is_success:
				file_path = result.data
				file_path_new = file_path.replace('.wav', '.mp3')
				file_mp3 = AudioSegment.from_wav(file_path).export(file_path_new, format='mp3')
				filename_new = call_audio.filename.replace('.wav', '.mp3')
				CommonService.delete_temp_file(call_audio.filename)
				# upload to Disk
				disk_service = DiskService(user.userprofile.token)
				upload_result = disk_service.upload_file(File(file_mp3, filename_new), settings.CALL_RECORDS_DISK_FOLDER)
				if upload_result.is_success:
					# delete source file and save to db
					CommonService.delete_temp_file(filename_new)
					call.record_filename = upload_result.data
					call.save()
					return ServiceResponse(True, data=call.record_filename)
		return ServiceResponse(False)

	@staticmethod
	def get_call_record_filename(call_id, user):
		"""
		Get call record filename by call_id
		:param call_id: id of the call
		:param user: current user
		:return: call record
		"""
		result = DBService.get_call(call_id=call_id)

		if result.is_success:
			call = result.data
			# check if current user is the master of the call
			if call.user_profile_id != user.userprofile.pk:
				ServiceResponse(False, message=Code.PMDERR)
			# check if the record was already loaded
			filename = call.record_filename
			if not filename:
				load_result = PBXDataService.load_call_record_file(call, user)
				if load_result.is_success:
					filename = load_result.data
				else:
					return ServiceResponse(False)
			return ServiceResponse(True, data=filename)
		return ServiceResponse(False, data=result.data, message=result.message)

	@staticmethod
	def get_call_record_download_link(call_id, user):
		"""
		Get call record download link by call_id
		:param call_id: id of the call
		:param user: current user
		:return: call record download link
		"""
		result = PBXDataService.get_call_record_filename(call_id, user)
		if result.is_success:
			filename = result.data
			disk_service = DiskService(user.userprofile.token)
			result = disk_service.get_download_link(filename, settings.CALL_RECORDS_DISK_FOLDER)
			if result.is_success:
				return ServiceResponse(True, data=result.data, message=filename)
		return ServiceResponse(False, data=result.data, message=result.message)

	@staticmethod
	def get_call_record_file(call_id, user):
		"""
		Get call record file by call_id
		:param call_id: id of the call
		:param user: current user
		:return: call record File instance
		"""
		result = PBXDataService.get_call_record_download_link(call_id, user)
		if result.is_success:
			link = result.data
			filename = result.message
			disk_service = DiskService(user.userprofile.token)
			result = disk_service.download_file(link, filename)
			if result.is_success:
				if result.is_success:
					return ServiceResponse(True, data=result.data)
		return ServiceResponse(False, data=result.data, message=result.message)