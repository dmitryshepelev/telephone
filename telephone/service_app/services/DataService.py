import json
import datetime

import requests

from telephone import settings
from telephone.classes.Call import Call, CallATS, CallRecord
from telephone.classes.ServiceResponse import ServiceResponse
from telephone.service_app.services.CommonService import CommonService
from telephone.service_app.services.LogService import Code
from telephone.main_app.models import Call as CallModel


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
	def update_calls_list(params, ats_params, user):
		stat_result = DataService.get_statistics(params, user)
		stat_ats_result = DataService.get_ats_statistic(ats_params, user)
		if stat_result.is_success and stat_ats_result.is_success:
			merged_stat = DataService.merge_calls(stat_result.data, stat_ats_result.data)
			user_stat = user.userprofile.call_set.filter(date__gte=datetime.datetime.today())
			if merged_stat and len(user_stat) != len(merged_stat):
				for s in merged_stat:
					stat_record = user_stat.filter(call_id=s.call_id)
					if not stat_record:
						stat_record = CallModel(
							call_id=s.call_id,
							sip=s.sip,
							date=s.date,
							destination=s.destination,
							description=s.description,
							disposition=s.disposition,
							bill_seconds=s.bill_seconds,
							cost=s.cost,
							bill_cost=s.bill_cost,
							currency=s.currency,
							user_profile=user.userprofile
						)
						stat_record.save()
			return ServiceResponse(True)
		return ServiceResponse(False, message=Code.UCLSWR)