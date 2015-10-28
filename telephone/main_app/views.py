# coding=utf-8

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from telephone.classes.ApiParams import ApiParams
from telephone.classes.Call import CallRecord, CallsStat
from telephone.classes.FilterParams import CallsFilterParams
from telephone.service_app.services.PBXDataService import PBXDataService
from telephone.service_app.services.LogService import LogService, Code


logger = LogService()


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
	params = ApiParams(request.GET or None)

	update_res = PBXDataService.update_calls_list(params, request.user)
	logger.info(Code.UCLEXE, is_success=update_res.is_success, status_code=update_res.status_code, message=update_res.message, data=update_res.data)

	filter_params = CallsFilterParams(request.GET)
	calls = [CallRecord(call=call) for call in request.user.userprofile.call_set.filter(**filter_params.params).order_by('date')]
	calls_stat = CallsStat(calls)
	return render_to_response(template, {'calls': calls, 'calls_stat': calls_stat}, context_instance=RequestContext(request))


@login_required
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