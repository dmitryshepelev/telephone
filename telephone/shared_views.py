from django.shortcuts import render_to_response


def default_404(request):
	"""
	default 404 page
	:param request: HTTP GET request
	:param request: html template
	:return: HttpResponse instance
	"""
	return render_to_response('default_404.html')


