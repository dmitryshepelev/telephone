import json

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, JsonResponse

from telephone.classes.Parameters import MailParameters
from telephone.service_app.services.CommonService import CommonService
from telephone.service_app.services.ApiService import ApiService
from telephone.service_app.services.LogService import LogService, Code

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
@user_passes_test(lambda user: user.is_superuser)
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