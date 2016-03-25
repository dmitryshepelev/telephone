from telephone.classes.ServerResponse import ServerResponse
from telephone.classes.ApiParams import ApiParams
from telephone.classes.Call import CallRecord, CallsStat
from telephone.classes.FilterParams import CallsFilterParams
from telephone.service_app.services.CommonService import CommonService
from telephone.service_app.services.PBXDataService import PBXDataService


def get_statistic(request):
	"""
	Controller to get test calls file
	:param request: HTTP GET request
	:param template: html template
	:return: json format
	"""
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
	if not request.user.is_authenticated():
		return ServerResponse.unauthorized()

	from_number = CommonService.reduce_number(request.GET.get('fromN') or request.user.userprofile.sip)
	to_number = request.GET.get('toN')

	if not to_number:
		return ServerResponse.bad_request(message='Target number is not defined')

	to_number = CommonService.reduce_number(to_number)

	# result = PBXDataService.request_callback(request.user, from_number, to_number)
	result = {'status': 'ok'}
	if result:
		return ServerResponse.ok(data={'info': result})

	return ServerResponse.internal_server_error()