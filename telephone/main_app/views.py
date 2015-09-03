# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from telephone import settings
from telephone.exceptions import ApiErrorException, MailErrorException
from telephone.main_app.forms import NewUserForm
from telephone.main_app.proxy.Parameters import CallsParameters, MailParameters
from telephone.main_app.services import get_logger,	create_domain_mail
from telephone import services
from telephone.service_app.services.api_service import ApiService
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
	"""
	Create new user controller
	:param request: HTTP request
	:param template: html template
	:return:
	"""
	if request.user.is_superuser:  # TODO: is_superuser decorator

		if request.POST:
			new_user_form = NewUserForm(request.POST)
			if new_user_form.errors:
				return JsonResponse({'errors': new_user_form.errors})
			try:
				# user = services.create_profile(new_user_form.data)
				return HttpResponse(status=201)
			except Exception as e:
				# TODO: handle exception
				return HttpResponse(status=500)
		else:
			email_id = services.get_random_string(6, only_digits=True)
			response_params = {'email_id': email_id, 'password': ApiService.generate_email_password(email_id), 'domain': '@%s' % settings.DOMAIN}
			return render_to_response(template, response_params, context_instance=RequestContext(request))
	return default_404(request)


@login_required
def create_mail(request):
	"""
	Creates new email
	:param request: HTTP request
	:return: dict
	"""
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