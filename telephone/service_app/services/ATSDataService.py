import json
import requests

from telephone import settings
from telephone.classes.Call import Call, CallATS, CallRecord
from telephone.classes.ServiceResponse import ServiceResponse
from telephone.service_app.services.LogService import LogService
from telephone.service_app.services.CommonService import CommonService
from telephone.service_app.services.LogService import Code
from telephone.main_app.models import Call as CallModel


class ATSDataService():
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
			return ServiceResponse(api_response.ok, [CallATS(s) for s in json.loads(api_response.content)['stats']])
		return ServiceResponse(api_response.ok, status_code=api_response.status_code)

	@staticmethod
	def merge_calls(stat, stat_ATS):
		"""
		Merge statistic
		:param stat: calls statistic
		:param stat_ATS: ATS calls statistic
		:return: ServiceResponse
		"""
		result = []

		key_value = None
		group = []
		grouped = []
		for s in stat:
			if not key_value:
				key_value = s.date
			if abs(key_value - s.date).seconds < settings.TIME_CORRECTION or not group:
				group.append(s)
			else:
				grouped.append(group)
				group = [s]
				key_value = s.date
			if s == stat[-1] and group:
				grouped.append(group)

		stat_filtered = []
		for __group in grouped:
			record = __group[0]
			if len(__group) > 1:
				records = filter(lambda x: x.disposition == 'answered', __group)
				if records:
					record = records[0]
			stat_filtered.append(record)
		for stat_filtered_record in stat_filtered:
			stat_ATS_filtered = filter(lambda y: y.destination == stat_filtered_record.destination, stat_ATS)
			for stat_ATS_filtered_record in stat_ATS_filtered:
				if abs(stat_ATS_filtered_record.date - stat_filtered_record.date).seconds < settings.TIME_CORRECTION:
					result.append(CallRecord(stat_filtered_record, stat_ATS_filtered_record))
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
		stat_common_res = ATSDataService.get_common_stat(params, user)
		if not stat_common_res.is_success:
			return ServiceResponse(False, message=Code.UCLUNS, data={'params': params, 'user_id': user.pk}, status_code=stat_common_res.status_code)

		# get pbx stat
		stat_pbx_res = ATSDataService.get_pbx_stat(params, user)
		if not stat_pbx_res.is_success:
			return ServiceResponse(False, message=Code.UCLUNS, data={'params': params, 'user_id': user.pk}, status_code=stat_pbx_res.status_code)

		merged_stat = ATSDataService.merge_calls(stat_common_res.data, stat_pbx_res.data)
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
							user_profile=user.userprofile
						)
						stat_record.save()
					except Exception as e:
						update_errors.append((stat_record, e.message,))
			if update_errors:
				message += Code.UCLSWE
		else:
			message = Code.UCLNTU.value
		return ServiceResponse(True, data=update_errors, message=message)