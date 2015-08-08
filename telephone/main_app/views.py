import os

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from telephone.main_app import Schema

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
def get_test_file(request):
	"""
	Controller to get test calls file
	:param request: HTTP GET request
	:return: csv file
	"""
	abspath = open(BASE_DIR + '/static/content/test.csv', 'r')
	response = HttpResponse(content=abspath.read())
	response['Content-Type'] = 'text'
	return response


@login_required
def get_test_record(request):
	"""
	Controller to get test call record file
	:param request: HTTP GET request
	:return: mp3 file
	"""
	path = BASE_DIR + '/static/content/test.mp3'
	response = HttpResponse(content=open(path, 'rb'), content_type='audio/mp3')
	response['Content-Length'] = os.path.getsize(path)
	response['Content-Disposition'] = 'attachment; filename=%s' % 'test.mp3'
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