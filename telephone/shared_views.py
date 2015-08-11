from django.shortcuts import render_to_response
from django.template import RequestContext

from telephone.services import AppLogger


logger = AppLogger('app_logger')


def default_404(request):
	"""
	default 404 page
	:param request: HTTP GET request
	:param request: html template
	:return: HttpResponse instance
	"""
	logger.warning('404 not found', request.path, request, None)
	return render_to_response('default_404.html')


def default_error(request, template):
	"""
	default error page
	:param request: HTTP GET request
	:param template: html template
	:return: HttpResponse instance
	"""
	logger.warning('Default error', request.path, request, None)
	return render_to_response(template, {}, context_instance=RequestContext(request))