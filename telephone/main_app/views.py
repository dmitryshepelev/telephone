# coding=utf-8
import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from telephone.classes.ApiParameters import StatApiParameters, StatATSApiParameters
from telephone.main_app.models import Call
from telephone.main_app.services import get_logger
from telephone import services
from operator import itemgetter
from itertools import groupby
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
	:param template: html template
	:return: json format
	"""
	params = request.GET or None

	stat_params = StatApiParameters(params)
	stat_ats_params = StatATSApiParameters(params)
	if stat_params.end == datetime.datetime.now().strftime(settings.DATETIME_FORMAT_END):
		DataService.update_calls_list(stat_params, stat_ats_params, request.user)
	stat_result = DataService.get_statistics(stat_params, request.user)

	stat_ats_params = StatATSApiParameters(params)
	stat_ats_result = DataService.get_ats_statistic(stat_ats_params, request.user)

	if stat_result.is_success and stat_ats_result.is_success:
		calls = DataService.merge_calls(stat_result.data, stat_ats_result.data)

		return render_to_response(template, {'calls': calls}, context_instance=RequestContext(request))
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