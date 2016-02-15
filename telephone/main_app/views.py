# coding=utf-8
import datetime
import json
import os
from io import open

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import requests

from telephone import settings
from telephone.admin_app.views import panel
from telephone.classes.ApiParams import ApiParams
from telephone.classes.Call import CallRecord, CallsStat
from telephone.classes.FilterParams import CallsFilterParams
from telephone.classes.PaymentData import PaymentData
from telephone.classes.SubscriptionData import SubscriptionData
from telephone.main_app.models import UserProfile, WidgetScript
from telephone.service_app.services.CommonService import CommonService
from telephone.service_app.services.DBService import DBService
from telephone.service_app.services.PBXDataService import PBXDataService
from telephone.service_app.services.LogService import LogService, Code


logger = LogService()


def main_resolver(request, templates):
	"""
	Controller to show main page
	:param request: HTTP GET request
	:param templates: html templates
	:return: HttpResponse instance
	"""
	if request.user.is_authenticated() and request.user.is_superuser:
		return panel(request, templates[0])
	return calls(request, templates[1])


@login_required
@user_passes_test(lambda user: user.userprofile.date_subscribe_ended and (user.userprofile.date_subscribe_ended.date() - datetime.datetime.now().date()).days >= 0, login_url='/pay/subfee/', redirect_field_name='')
def calls(request, template):
	"""
	Controller to show calls page
	:param request: HTTP GET request
	:param template: html template
	:return: HttpResponse instance
	"""
	return render_to_response(template, {}, context_instance=RequestContext(request))


@login_required
def pay(request, type):
	"""
	Controller to pay
	:param request: HTTP request
	:param type: pay type
	:return: HttpResponse instance
	"""
	if request.method == 'GET':
		return render_to_response('pay_{type}.html'.format(type=type), {'subscription_data': SubscriptionData(), 'payment_data': PaymentData(request.user.userprofile.customer_number)}, context_instance=RequestContext(request))
	elif request.method == 'POST' and type == 'subfee':
		if request.POST:
			subscr = DBService.create_subscr_transaction(request.user, request.POST)
			if subscr:
				return HttpResponse(status=201)
	return HttpResponse(status=500)


@login_required
@user_passes_test(lambda user: user.userprofile.date_subscribe_ended and (user.userprofile.date_subscribe_ended.date() - datetime.datetime.now().date()).days >= 0, login_url='/pay/subfee/', redirect_field_name='')
def get_statistic(request, template):
	"""
	Controller to get test calls file
	:param request: HTTP GET request
	:param template: html template
	:return: json format
	"""
	params = ApiParams(request.GET or None)

	update_res = PBXDataService.update_calls_list(params, request.user)
	logger.info(Code.UCLEXE, is_success=update_res.is_success, status_code=update_res.status_code, message=update_res.message, data=update_res.data)

	filter_params = CallsFilterParams(request.GET)
	calls = [CallRecord(call=call) for call in request.user.userprofile.call_set.filter(**filter_params.params).exclude(**filter_params.exclude_params).filter(filter_params.call_type_query).order_by('date')]
	calls_stat = CallsStat(calls)
	return render_to_response(template, {'calls': calls, 'calls_stat': calls_stat}, context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda user: user.userprofile.date_subscribe_ended and (user.userprofile.date_subscribe_ended.date() - datetime.datetime.now().date()).days >= 0, login_url='/pay/subfee/', redirect_field_name='')
def get_call_record(request):
	"""
	Controller to get test call record file
	:param request: HTTP GET request
	:return: wav file
	"""
	call_id = request.GET.get('call_id') or None
	if not call_id:
		return HttpResponse(status=400)

	file_instance = PBXDataService.get_call_record_file(call_id, request.user)
	if not file_instance:
		return HttpResponse(status=500)

	response = HttpResponse(content_type='audio/mp3')
	response['Content-Disposition'] = 'attachment; filename={filename}'.format(filename=file_instance.filename)
	response.content = file_instance.content
	return response


@login_required
@user_passes_test(lambda user: not user.is_superuser)
def get_call_cost(request):
	"""
	Request to the api to get call cost by target phone number
	:param request: HTTP request
	:return: HttpResponse Instance
	"""
	to = request.GET.get('n')
	if not to:
		return HttpResponse(status=400)

	if len(to) < 6:
		return JsonResponse({'phone': to, 'notAvalible': True})

	result = PBXDataService.get_call_cost(request.user, CommonService.reduce_number(to))
	if result:
		result['phone'] = to
		return JsonResponse(result)

	return HttpResponse(status=500)


@login_required
@user_passes_test(lambda user: not user.is_superuser)
def request_callback(request):
	"""
	Request the callback
	:param request: HTTP request
	:return: HttpResponse instance
	"""
	from_number = CommonService.reduce_number(request.GET.get('cbFromNumber') or request.user.userprofile.sip)
	to_number = CommonService.reduce_number(request.GET.get('cbToNumber'))

	result = PBXDataService.request_callback(request.user, from_number, to_number)
	if result:
		return HttpResponse(status=200, content=result)

	return HttpResponse(status=500)


@login_required
@user_passes_test(lambda user: not user.is_superuser)
def get_call_cost_by_country(request):
	"""
	Returns call costs by country
	:param request: HTTP request
	:return: HttpResponse instance
	"""
	country = request.GET.get('country', 'россия').lower()

	result = requests.post('https://zadarma.com/ru/checks/call-cost/', {'number': country}, headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Cookie': 'currency=RUB; lang=en;'})
	data = json.loads(result.content)

	if result.ok:
		return JsonResponse(data)

	return HttpResponse(status=500, content=data)


@csrf_exempt
@require_http_methods(['POST', 'GET'])
def incoming_detect(request, user_key):
	"""
	Incoming calls information
	https://github.com/zadarma/user-api-v1/blob/master/examples/callinfo_callback.php
	:param request: HTTP request
	:return:
	"""
	if 'zd_echo' in request.GET.keys() and (request.GET.get('zd_echo') and not request.GET.get('zd_echo') == ''):
		logger.info('ECHO PASSED', zd_echo=request.GET.get('zd_echo'))
		return HttpResponse(str(request.GET.get('zd_echo')))

	if settings.DEBUG:
		caller_id = request.body.split('\n')[0].split(': ')[1]
		called_did = request.body.split('\n')[1].split(': ')[1]
		call_start = request.body.split('\n')[2].split(': ')[1]
	else:
		caller_id = request.POST.get('caller_id')
		called_did = request.POST.get('called_did')
		call_start = request.POST.get('call_start')

	logger.info('IC PARMS', params=(caller_id, called_did, call_start,))

	if not caller_id or not called_did or not call_start:
		return HttpResponse(status=400)

	# TODO: check signature
	# headers = request.META
	#
	# if 'Signature' in headers.keys():
	# 	print('IC Signature', headers.get('Signature'))
	# 	logger.info('IC HEDRS', signature=headers.get('Signature'))

	user_profile = UserProfile.objects.get(user_key=user_key)
	script = user_profile.widgetscript

	incoming_info = DBService.create_incoming_info(caller_id, called_did, datetime.datetime.strptime(call_start, settings.DATETIME_FORMAT_ALTER), script.guid)

	return HttpResponse(status=200)


@require_http_methods(['GET'])
def check_incoming_info(request, guid):
	"""
	Chech incoming call info
	:param request:
	:param guid:
	:return:
	"""
	try:
		script = WidgetScript.objects.get(guid=guid)
	except ObjectDoesNotExist as e:
		return HttpResponse(status=400)

	incoming_info = DBService.get_incoming_info(script.guid)

	response = HttpResponse()
	response['Access-Control-Allow-Origin'] = '*'

	if not incoming_info:
		response.status_code = 204
		return response

	incoming_info.is_taken = True
	incoming_info.save()

	response.status_code = 200
	response.content = {'status': 1}
	return response


@require_http_methods(['GET', 'POST'])
@login_required
def get_widget_script(request):
	"""
	Return widget script
	:param request:
	:return:
	"""
	if request.method == 'GET':
		return render_to_response('get_script.html', {}, context_instance=RequestContext(request))

	widget = request.user.userprofile.widgetscript
	#
	source_file = os.path.join(settings.BASE_DIR, 'static/content/scripts/common/widget.js')
	temp_path = os.path.join(settings.BASE_DIR, settings.TEMP_DIR)
	filename = request.user.username + '_' + widget.guid + '.js'

	CommonService.delete_temp_file(filename)

	with open(temp_path + request.user.username + '_' + widget.guid + '.min.js', 'w+') as temp_file:
		with open(source_file, 'r') as s_f:
			for line in s_f:
				temp_file.write(line.replace('{{widget_guid}}', widget.guid))

	response = HttpResponse(content_type='application/x-javascript')
	response['Content-Disposition'] = 'attachment; filename={filename}'.format(filename=filename)
	response.content = open(temp_path + request.user.username + '_' + widget.guid + '.min.js', 'r').read()
	return response