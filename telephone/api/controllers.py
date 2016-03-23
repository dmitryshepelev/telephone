from telephone.classes.ServerResponse import ServerResponse
from telephone.classes.ApiParams import ApiParams
from telephone.classes.Call import CallRecord, CallsStat
from telephone.classes.FilterParams import CallsFilterParams
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
