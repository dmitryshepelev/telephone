from itertools import groupby
import json
import requests
from telephone import settings
from telephone.classes.Call import Call, CallATS, CallRecord
from telephone.classes.ServiceResponse import ServiceResponse
from telephone.service_app.services.CommonService import CommonService


class DataService():
	def __init__(self):
		pass

	@staticmethod
	def get_statistics(params, user):
		"""
		Get statistics from api
		:param params: CallParameters instance
		:param user: User instance
		:return: json type
		"""
		if settings.TEST_MODE or user.is_superuser:
			abspath = open(settings.BASE_DIR + '/static/content/stat.csv', 'r')
			data_arr = CommonService.parse_csv(abspath.read())
			return ServiceResponse(True, [Call(d) for d in data_arr])

		api_response = requests.get(params.request_string, headers={'Authorization': '%s:%s' % (user.userprofile.user_key, params.get_sign(user.userprofile.secret_key))})
		if api_response.ok:
			return ServiceResponse(api_response.ok, [Call(s) for s in json.loads(api_response.content)['stats']])
		return ServiceResponse(api_response.ok, message=api_response.status_code)

	@staticmethod
	def get_ats_statistic(params, user):
		"""
		Get ats statistics from api
		:param params: CallParameters instance
		:param user: User instance
		:return: json type
		"""
		api_response = requests.get(params.request_string, headers={'Authorization': '%s:%s' % (user.userprofile.user_key, params.get_sign(user.userprofile.secret_key))})
		if api_response.ok:
			return ServiceResponse(api_response.ok, [CallATS(s) for s in json.loads(api_response.content)['stats']])
		return ServiceResponse(api_response.ok, message=api_response.status_code)

	@staticmethod
	def merge_calls(stat, stat_ATS):
		"""
		Merge statistic
		:param stat: calls statistic
		:param stat_ATS: ATS calls statistic
		:return: ServiceResponse
		"""
		result = []
		stat_filtered = []

		key_value = None
		group = []
		grouped = []
		for s in stat:
			if not key_value:
				key_value = s.date
			if abs(key_value - s.date).seconds < 3 or not group:
				group.append(s)
			else:
				grouped.append(group)
				group = [s]
				key_value = s.date
				# TODO: last elements

		for key, group in groupby(stat, lambda s: s.date):
			__group = [g for g in group]
			record = __group[0]
			if len(__group) > 1:
				records = filter(lambda x: x.disposition == 'answered', __group)
				if records:
					record = records[0]
			stat_filtered.append(record)
		for stat_filtered_record in stat_filtered:
			stat_ATS_filtered = filter(lambda y: y.destination == stat_filtered_record.destination, stat_ATS)
			for stat_ATS_filtered_record in stat_ATS_filtered:
				if abs(stat_ATS_filtered_record.date - stat_filtered_record.date).seconds < 3:
					result.append(CallRecord(stat_filtered_record, stat_ATS_filtered_record))
		return ServiceResponse(True, result)