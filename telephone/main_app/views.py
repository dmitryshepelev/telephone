import os

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import requests

from telephone import settings
from telephone.main_app.services import get_request_string
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
	return render_to_response(template, {}, context_instance=RequestContext(request))


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
	request = requests.get(url, headers={'Content-Disposition': 'attachment', 'filename': 'stat_%s-%s' % (request.GET.get('form'), request.GET.get('to'))})
	response.content = request.content[:-1] if request.content[-1] == '\n' else request.content
	return response


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
	request = requests.get(url, headers={'Content-Disposition': 'attachment', 'filename': '%s.mp3' % (record_id,)})
	response.content = request.content
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