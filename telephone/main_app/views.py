# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from telephone.classes.Parameters import CallsParameters
from telephone.main_app.services import get_logger
from telephone import services
from json import loads
from telephone.service_app.services.DataService import DataService


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
	return render_to_response(template, {}, context_instance=RequestContext(request))


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
	result = DataService.get_statistics(params, request.user)
	params.set_method(True)
	result_pbx = DataService.get_statistics(params, request.user)
	if result.is_success:
		return render_to_response(template, {'calls': result.data}, context_instance=RequestContext(request))
	# TODO: Logger
	return HttpResponse(status=500)


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