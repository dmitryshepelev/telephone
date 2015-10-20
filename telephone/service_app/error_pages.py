from django.shortcuts import render_to_response
from django.template import RequestContext


def default_error(request, template):
	"""
	default error page
	:param request: HTTP GET request
	:param template: html template
	:return: HttpResponse instance
	"""
	return render_to_response(template, {}, context_instance=RequestContext(request))