import os

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import requests

from telephone import settings
from telephone.main_app import services
from telephone.main_app.services import get_request_string, get_logger, parse_csv
from telephone.settings import BASE_DIR


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
	schema_name = request.user.userprofile.schema.name
	calls_list = services.get_calls(request)
	return render_to_response(template, {'schema_name': schema_name, 'calls': calls_list}, context_instance=RequestContext(request))


@login_required
def get_calls(request):
	"""
	Controller to get test calls file
	:param request: HTTP GET request
	:return: csv file
	"""
	response = HttpResponse(content_type='text')

	if settings.TEST_MODE or request.user.is_superuser:
		abspath = open(BASE_DIR + '/static/content/test.csv', 'r')
		response.content = abspath.read()
		return response

	request_string = get_request_string(request.GET)
	url = '%s%s%s' % (settings.API_URLS['base_api_url'], settings.API_URLS['get_calls'], request_string,)
	api_request = requests.get(url, headers={'Content-Disposition': 'attachment', 'filename': 'stat_%s-%s' % (request.GET.get('form'), request.GET.get('to'))})
	if api_request.ok:
		response.content = api_request.content[:-1] if api_request.content[-1] == '\n' else api_request.content
		return response
	else:
		get_logger().error('api data export request error', request.path, request, {'Schema code': request.user.userprofile.schema.schema_code, 'Request string': request_string})
		return HttpResponse(status=500)


@login_required
def get_call_record(request):
	"""
	Controller to get test call record file
	:param request: HTTP GET request
	:return: mp3 file
	"""
	response = HttpResponse(content_type='audio/mp3')

	if settings.TEST_MODE or request.user.is_superuser:
		path = BASE_DIR + '/static/content/test.mp3'
		response.content = open(path, 'rb')
		response['Content-Length'] = os.path.getsize(path)
		response['Content-Disposition'] = 'attachment; filename=%s' % 'test.mp3'
		return response

	record_id = request.GET.get('id')
	request_string = get_request_string({'id': record_id, 'user': request.user.userprofile.user_code})
	url = '%s%s%s' % (settings.API_URLS['base_api_url'], settings.API_URLS['get_record'], request_string,)
	api_request = requests.get(url, headers={'Content-Disposition': 'attachment', 'filename': '%s.mp3' % (record_id,)})
	if api_request.ok:
		response.content = api_request.content
		return response
	else:
		get_logger().error('api call record request error', request.path, request, {'Schema code': request.user.userprofile.schema.schema_code, 'Request string': request_string})
		return HttpResponse(status=500)


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