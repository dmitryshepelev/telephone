from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from telephone.main_app import services
from telephone.main_app.proxy.Parameters import Parameters
from telephone.main_app.services import get_logger


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
def get_calls(request, template):
	"""
	Controller to get test calls file
	:param request: HTTP GET request
	:return: csv file
	"""
	params = Parameters()
	if request.GET:
		params.set_params(request.GET)
	params.set_params({'user': request.user.userprofile.user_code})
	calls_list = services.get_calls(params, request.user.is_superuser)
	if calls_list is None:
		get_logger().error('Get calls error', request.path, request, params.get_params())
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
def get_period_modal_template(request, template):
	"""
	Get html template of the period modal
	:param request: HTTP GET request
	:param template: html template
	:return: HttpResponse instance
	"""
	return render_to_response(template, {}, context_instance=RequestContext(request))


@login_required
def schema_error(request, template):
	"""
	Schema error page
	:param request: HTTP GET request
	:param template: html template
	:return: HttpResponse instance
	"""
	return render_to_response(template, {}, context_instance=RequestContext(request))