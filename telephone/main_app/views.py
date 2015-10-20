# coding=utf-8

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from telephone.classes.ApiParams import ApiParams
from telephone.classes.Call import CallRecord
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
	return render_to_response(template, {'calls': calls}, context_instance=RequestContext(request))


# @login_required
# def get_call_record(request):
# 	"""
# 	Controller to get test call record file
# 	:param request: HTTP GET request
# 	:return: mp3 file
# 	"""
# 	params = {'user': request.user.userprofile.user_code}
# 	if request.GET:
# 		params['id'] = request.GET.get('id')
# 	record = services.get_call_record(params, request.user.is_superuser)
# 	if not record:
# 		get_logger().error('Get record error', request.path, request, params)
# 		return HttpResponse(status=500)
# 	response = HttpResponse(content_type='audio/mp3')
# 	response['Content-Disposition'] = 'attachment; filename=%s' % 'record.mp3'
# 	response.content = record
# 	return response