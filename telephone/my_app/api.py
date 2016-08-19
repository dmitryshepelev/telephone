# coding=utf-8
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from telephone.decorators import api_authorized
from telephone.libs.Message import Message
from telephone.libs.ServerResponse import ServerResponse
from telephone.my_app.services.PBXService import PBXService, StatParams, CallStatusQuery, CallTypeQuery
from telephone.my_app.services.ServiceBase import ServiceResultError
from telephone.my_app.utils import DateTimeUtil


@require_http_methods(['GET'])
@api_authorized()
def get_pbx_info(request):
	"""
	Returns PBX profile info
	:param request:
	:return:
	"""
	data = {
		'username': request.user.username,
		'phone': request.user.pbx.phone_number
	}
	return ServerResponse.ok(data = data)


@require_http_methods(['GET'])
@api_authorized()
def get_stat(request):
	"""
	Returns stats
	:param request:
	:return:
	"""
	user = request.user
	stat_params = StatParams(
		start = DateTimeUtil.from_timestamp(request.GET.get('start', DateTimeUtil.to_timestamp(timezone.now()))),
		end = DateTimeUtil.from_timestamp(request.GET.get('end', DateTimeUtil.to_timestamp(timezone.now()))),
		status = request.GET.get('status', 0),
		call_type = request.GET.get('call_type', ''),
	)

	service = PBXService(user.pbx)
	service.update_stat(stat_params)

	status_query = CallStatusQuery(stat_params.status)
	types_query = CallTypeQuery(stat_params.call_type)

	calls = user.pbx.pbxcall_set.filter(types_query.query, status_query.query, date__gte = stat_params.start, date__lte = stat_params.end)

	return ServerResponse.ok(data = {'calls': [call.serialize() for call in calls]})


@require_http_methods(['GET'])
@api_authorized()
def get_call_cost(request):
	"""
	Get call cost
	:param request:
	:return:
	"""
	number = request.GET.get('n', '')

	service = PBXService(request.user.pbx)

	try:
		call_cost_info = service.get_call_cost(number)
		return ServerResponse.ok(data = {'call_cost_info': call_cost_info})

	except ServiceResultError as e:
		return ServerResponse.internal_server_error(message = Message.error('Повторите операцию позже'))


@require_http_methods(['GET'])
@api_authorized()
def get_call_record_file(request):
	"""
	Gets call's record file if exist
	:param request:
	:return:
	"""
	call_id = request.GET.get('cid', None)
	if not call_id:
		return ServerResponse.bad_request(message = Message.error('Неправильно заданы параметры'))

	pbx = request.user.pbx
	try:
		call = pbx.pbxcall_set.get(call_id = call_id)
	except ObjectDoesNotExist as e:
		return ServerResponse.not_found(message = Message.error('Звонка не существует в природе'))

	service = PBXService(pbx)
	file_instance = service.get_call_record_file(call)

	file_instance.filename = call_id

	response = HttpResponse(content_type = 'audio/mp3')
	response['Content-Disposition'] = 'attachment; filename=record-{username}-{filename}.mp3'.format(username = request.user.username, filename = file_instance.filename)
	response.content = file_instance.content
	return response


@require_http_methods(['GET'])
@api_authorized()
def get_costs_by_country(request):
	"""
	Get cost price list by country
	:param request:
	:return:
	"""
	country = request.GET.get('country', None)
	if not country:
		return ServerResponse.bad_request(message = Message.error('Не указана страна для запроса'))

	pbx = request.user.pbx

	service = PBXService(pbx)
	price_list = service.get_costs_by_country(country)

	return ServerResponse.ok(data = {'country': price_list.country, 'costs': price_list.price_list})
