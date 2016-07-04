# coding=utf-8
import json
import requests
from telephone.libs.ApiParams import ApiParams
from telephone.libs.Call import CallRecord, CallsStat
from telephone.libs.FilterParams import CallsFilterParams
from telephone.service_app.services.CommonService import CommonService
# from telephone.service_app.services.PBXDataService import PBXDataService


def get_statistic(request):
	"""
	Controller to get test calls file
	:param request: HTTP GET request
	:param template: html template
	:return: json format
	"""
	from telephone.libs.ServerResponse import ServerResponse
	if not request.user.is_authenticated():
		return ServerResponse.unauthorized()

	params = ApiParams(request.GET or None)

	update_res = PBXDataService.update_calls_list(params, request.user)

	filter_params = CallsFilterParams(request.GET)
	calls = [CallRecord(call=call) for call in request.user.userprofile.call_set.filter(**filter_params.params).exclude(**filter_params.exclude_params).filter(filter_params.call_type_query).order_by('-date')]
	calls_stat = CallsStat(calls)

	data = {
		'calls': [call.vm() for call in calls],
		'calls_stat': calls_stat.vm()
	}

	return ServerResponse.ok(data=data)


def get_call_cost(request):
	"""
	Request to the api to get call cost by target phone number
	:param request: HTTP request
	:return: HttpResponse Instance
	"""
	from telephone.libs.ServerResponse import ServerResponse
	if not request.user.is_authenticated():
		return ServerResponse.unauthorized()

	to = request.GET.get('n')
	if not to:
		return ServerResponse.bad_request(message='Number must be defined')

	if len(to) < 6:
		return ServerResponse.bad_request(data={'phone': to, 'notAvalible': True})

	result = PBXDataService.get_call_cost(request.user, CommonService.reduce_number(to))
	if result:
		result['phone'] = to
		return ServerResponse.ok(data={'info': result})

	return ServerResponse.internal_server_error()


def cb_call(request):
	"""
	Request the callback
	:param request: HTTP request
	:return: HttpResponse instance
	"""
	from telephone.libs.ServerResponse import ServerResponse
	if not request.user.is_authenticated():
		return ServerResponse.unauthorized()

	from_number = CommonService.reduce_number(request.GET.get('fromN') or request.user.userprofile.sip)
	to_number = request.GET.get('toN')

	if not to_number:
		return ServerResponse.bad_request(message='Target number is not defined')

	to_number = CommonService.reduce_number(to_number)

	result = PBXDataService.request_callback(request.user, from_number, to_number)
	if result:
		return ServerResponse.ok(data={'info': result})

	return ServerResponse.internal_server_error()


def get_call_cost_by_country(request):
	"""
	Returns call costs by country
	:param request: HTTP request
	:return: HttpResponse instance
	"""
	from telephone.libs.ServerResponse import ServerResponse
	if not request.user.is_authenticated():
		return ServerResponse.unauthorized()

	country = request.GET.get('country', 'россия').lower()

	result = requests.post('https://zadarma.com/ru/checks/call-cost/', {'number': country}, headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Cookie': 'currency=RUB; lang=en;'})
	data = json.loads(result.content)

	if result.ok:
		return ServerResponse.ok(data={'costs': data})

	return ServerResponse.bad_request(data={'data': data})