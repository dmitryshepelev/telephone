from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from telephone import settings

from telephone.main_app import services
from telephone.exceptions import ApiErrorException, MailErrorException
from telephone.main_app.proxy.Parameters import CallsParameters, MailParameters
from telephone.main_app.services import get_logger, get_random_number, generate_email_password, generate_random_password, \
	create_domain_mail, get_oauth_token
from telephone.shared_views import default_404


def main(request, template):
	"""
	Controller to show main page
	:param request: HTTP GET request
	:param template: html template
	:return: HttpResponse instance
	"""
	return render_to_response(template, {}, context_instance=RequestContext(request))


@login_required
def calls(request, template):
	"""
	Controller to show calls page
	:param request: HTTP GET request
	:param template: html template
	:return: HttpResponse instance
	"""
	return render_to_response(template, {'schema_name': request.user.userprofile.schema.name}, context_instance=RequestContext(request))


@login_required
def get_statistic(request, template):
	"""
	Controller to get test calls file
	:param request: HTTP GET request
	:return: json format
	"""
	params = CallsParameters()
	if request.GET:
		params.set_params(request.GET)
	try:
		calls_list = services.get_statistics(params, request.user)
	except ApiErrorException as e:
		get_logger().error(e.message, e.url, request, e.data)
		return HttpResponse(status=500)
	return render_to_response(template, {'calls': calls_list}, context_instance=RequestContext(request))


@login_required
def get_call_record(request):
	"""
	Controller to get test call record file
	:param request: HTTP GET request
	:return: mp3 file
	"""
	params = {'user': request.user.userprofile.user_code}
	if request.GET:
		params['id'] = request.GET.get('id')
	record = services.get_call_record(params, request.user.is_superuser)
	if not record:
		get_logger().error('Get record error', request.path, request, params)
		return HttpResponse(status=500)
	response = HttpResponse(content_type='audio/mp3')
	response['Content-Disposition'] = 'attachment; filename=%s' % 'record.mp3'
	response.content = record
	return response


@login_required
def schema_error(request, template):
	"""
	Schema error page
	:param request: HTTP GET request
	:param template: html template
	:return: HttpResponse instance
	"""
	return render_to_response(template, {}, context_instance=RequestContext(request))


@login_required
def create_new_user(request, template):
	if request.user.is_superuser:
		if request.POST:
			pass
		else:
			email_id = get_random_number(6)
			return render_to_response(template, {'email_id': email_id, 'password': generate_email_password(email_id), 'domain': '@%s' % settings.DOMAIN}, context_instance=RequestContext(request))
	return default_404(request)


@login_required
def generate_password(request):
	if request.user.is_superuser:
		return JsonResponse({'password': generate_random_password(10)})
	return default_404(request)


@login_required
def create_mail(request):
	if request.user.is_superuser and request.POST:
		params = MailParameters(request.POST)
		try:
			result = create_domain_mail(params)
			return JsonResponse({'login': result['login'], 'uid': result['uid']})
		except MailErrorException as e:
			# TODO: log exceptions
			# get_logger().error(e.message, e.url, request, e.data)
			return HttpResponse(status=500)
	return HttpResponse(status=500)


@login_required
def get_api_urls(request):
	if request.user.is_superuser and request.GET:
		reason = request.GET.get('reason')
		if reason == 'code':
			return JsonResponse({'url': '%s%s&client_id=%s' % (settings.API_URLS['oauth']['host'], settings.API_URLS['oauth']['authorize'], settings.O_AUTH_ID)})
	return HttpResponse(status=500)


@login_required
def get_api_token(request):
	if request.user.is_superuser and request.POST:
		try:
			result = get_oauth_token(request.POST.get('code'))
			return JsonResponse({'token': result['access_token']})
		except Exception as e:
			pass
			return HttpResponse(status=500)
	return HttpResponse(status=500)