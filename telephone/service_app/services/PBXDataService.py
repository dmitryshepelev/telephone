import json
import requests

from telephone import settings
from telephone.classes.Call import Call, CallRecord, CallPBX
from telephone.classes.ServiceResponse import ServiceResponse
from telephone.service_app.services.CommonService import CommonService, CallsConstants
from telephone.service_app.services.LogService import Code
from telephone.main_app.models import Call as CallModel


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
				call.set_params(call_id=c.call_id, bill_seconds=c.seconds)
			else:
				call.set_params(clid=c.clid, date=c.date, destination=c.destination, disposition=c.disposition, sip=c.sip)
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

		row_to_update = len(merged_stat) - len(user_stat)
		message = '{row_to_update} row(s) to be updated. '.format(row_to_update=row_to_update)
		update_errors = []
		if row_to_update > 0:
			for m_s in merged_stat:
				stat_record = user_stat.filter(call_id=m_s.call_id)
				if not stat_record:
					try:
						stat_record = CallModel(
							call_id=m_s.call_id,
							sip=m_s.sip,
							date=m_s.date,
							destination=m_s.destination,
							description=m_s.description,
							disposition=m_s.disposition,
							bill_seconds=m_s.bill_seconds,
							cost=m_s.cost,
							bill_cost=m_s.bill_cost,
							currency=m_s.currency,
							is_answered=m_s.is_answered,
							user_profile=user.userprofile
						)
						stat_record.save()
					except Exception as e:
						update_errors.append((stat_record, e.message,))
			if update_errors:
				message += Code.UCLSWE
		else:
			message = Code.UCLNTU
		return ServiceResponse(True, data=update_errors, message=message)