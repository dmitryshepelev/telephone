# coding=utf-8
import os
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from telephone import settings
from telephone.classes.MailMessage import MailMessage

from telephone.classes.MailParameters import MailParameters
from telephone.classes.TransactAction import TransactAction
from telephone.service_app.services.CommonService import CommonService
from telephone.service_app.services.ApiService import ApiService
from telephone.service_app.services.DBService import DBService
from telephone.service_app.services.LogService import LogService, Code
from telephone.service_app.services.ProfileService import ProfileService


logger = LogService()


@login_required
@user_passes_test(lambda user: user.is_superuser)
def get_api_urls(request):
	"""
	Api access url based on 'reason' GET parameter
	:param request: HTTP request
	:return: dict
	"""
	if request.GET:
		result = ApiService.get_url(request.GET.get('reason'))
		if result.is_success:
			return JsonResponse({'url': result.data})
	return HttpResponse(status=500)


@login_required
@user_passes_test(lambda user: user.is_superuser)
def get_oauth_token(request):
	"""
	Get OAuth token to api access
	:param request: HTTP request
	:return: dict
	"""
	if request.POST:
		code = request.POST.get('code')
		if code:
			result = ApiService.get_token(code)
			status_code = 200
			if not result.is_success:
				status_code = 400
				logger.error(Code.GTKERR, data=result.data, POST=request.POST)
			return JsonResponse(result.data, status=status_code)
	return HttpResponse(status=500)


@login_required
@user_passes_test(lambda user: user.is_superuser)
def generate_password(request):
	"""
	Generate random password
	:param request: HTTP request
	:return: dict with 'password' key
	"""
	return JsonResponse({'password': CommonService.get_random_string(10)})


@login_required
def get_transact_id(request):
	"""
	Get transact id
	:param request: HTTP request
	:return: guid
	"""
	return JsonResponse({'id': CommonService.get_guid()})


@login_required
@user_passes_test(lambda user: user.is_superuser)
@require_http_methods(['POST'])
def create_mail(request):
	"""
	Creates new email
	:param request: HTTP request
	:return: JsonResponse
	"""
	if request.POST:
		params = MailParameters(request.POST)
		result = ApiService.create_domain_mail(params)
		if result.is_success and result.data['success'] == 'ok':
			update_result = ApiService.update_mailbox_params(result.data['login'])
			if update_result.is_success:
				return JsonResponse({'login': result.data['login'], 'uid': result.data['uid']})
		logger.error(Code.MCRERR, data=result.data, POST=request.POST)
		return JsonResponse(result.data, status=400)
	return HttpResponse(status=500)


@login_required
@user_passes_test(lambda user: user.is_superuser)
def get_mailbox_data(request):
	"""
	Controller to get new mailbox data
	:param request: HTTP request
	:return: JsonResponse
	"""
	return JsonResponse(ApiService.generate_mailbox_data().data)


@login_required
@user_passes_test(lambda user: user.is_superuser)
@require_http_methods(['POST'])
def transact_action(request):
	"""
	Controller to execute transact action
	:param request: HTTP request
	:return: JsonResponse instance
	"""
	transact_id = request.POST.get('transactId')
	transact = DBService.get_transact(transact_id)
	if not transact:
		return HttpResponse(status=500)

	action = TransactAction(request.POST.get('actionId'))
	transact = action.execute(transact)
	if transact:
		if action.action_id == 1:
			ProfileService.extend_subscription(transact.user_profile, transact.duration)
			message = MailMessage(settings.INFO_EMAIL, 'Продление подписки', 'mail_tmpl_subscribe_extended.html', {'username': transact.user_profile.user.username, 'expiration_date': transact.user_profile.date_subscribe_ended}, transact.user_profile.user.email)
			message.send()
		return JsonResponse({'transactId': transact.transact_id})

	return HttpResponse(status=500)