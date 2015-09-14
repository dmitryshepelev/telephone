import json
import requests
from telephone import settings
from telephone.classes.Call import Call
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

		api_response = requests.get(params.get_request_string(), headers={'Authorization': '%s:%s' % (user.userprofile.user_key, params.get_sign(user.userprofile.secret_key))})
		if api_response.ok:
			return ServiceResponse(api_response.ok, [Call(s) for s in json.loads(api_response.content)['stats']])
		return ServiceResponse(api_response.ok, message=api_response.status_code)