# coding=utf-8
import datetime
import json

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import requests

from telephone import settings
from telephone.admin_app.views import panel
from telephone.classes.ApiParams import ApiParams
from telephone.classes.Call import CallRecord, CallsStat
from telephone.classes.FilterParams import CallsFilterParams
from telephone.classes.PaymentData import PaymentData
from telephone.classes.SubscriptionData import SubscriptionData
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
@user_passes_test(lambda user: user.userprofile.date_subscribe_ended and (user.userprofile.date_subscribe_ended.date() - datetime.datetime.now().date()).days >= 0, login_url='/pay/', redirect_field_name='')
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
@user_passes_test(lambda user: user.userprofile.date_subscribe_ended and (user.userprofile.date_subscribe_ended.date() - datetime.datetime.now().date()).days >= 0, login_url='/pay/', redirect_field_name='')
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
	calls = [CallRecord(call=call) for call in request.user.userprofile.call_set.filter(**filter_params.params).order_by('date')]
	calls_stat = CallsStat(calls)
	return render_to_response(template, {'calls': calls, 'calls_stat': calls_stat}, context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda user: user.userprofile.date_subscribe_ended and (user.userprofile.date_subscribe_ended.date() - datetime.datetime.now().date()).days >= 0, login_url='/pay/', redirect_field_name='')
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
def get_profile_info(request, template):
	"""
	Controller to get user account balance
	:param request: HTTP request
	:return: HttpResponse
	"""
	balance = PBXDataService.get_pbx_account_balance(request.user)
	if not balance:
		return HttpResponse(status=500)

	# 0 - subscribed, 1 - subscription ends in (or less than) 3 days, 2 - subscription ended
	date_subscribe_ended = request.user.userprofile.date_subscribe_ended
	if date_subscribe_ended:
		days_left = (date_subscribe_ended.date() - datetime.datetime.now().date()).days
		subscribe_ended_text = 'Подписка до ' + date_subscribe_ended.strftime(settings.DATE_CLIENT_FORMAT)
		if days_left >= 3:
			subscription_status = 0
		elif 0 <= days_left < 3:
			subscription_status = 1
		else:
			subscription_status = 2
			subscribe_ended_text = 'Подписка не оформлена'
	else:
		subscription_status = 2
		subscribe_ended_text = 'Подписка не оформлена'

	return render_to_response(template, {
			'balance': '%.2f' % balance,
			'subscribe_ended_text': subscribe_ended_text,
			'subscription_status': subscription_status,
		}, context_instance=RequestContext(request))


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

	result = PBXDataService.get_call_cost(request.user, to)
	if result:
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
	from_number = request.GET.get('cbFromNumber') or request.user.userprofile.sip
	to_number = request.GET.get('cbToNumber')

	result = PBXDataService.request_callback(request.user, from_number, to_number)
	if result:
		return HttpResponse(status=200)

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