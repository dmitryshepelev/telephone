import logging

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from telephone.auth_app.services import get_redirect_url, get_redirect_url_prop
from telephone.service_app.services.AuthService import AuthService


logger = logging.getLogger('auth_logger')


def login(request, template):
	"""
	Controller to show login page
	:param request: HTTP GET request
	:param template: html template
	:return: HttpResponse
	"""
	if request.POST:
		result = AuthService().sign_in(request)
		if not result.is_success:
			return HttpResponse(status=400, content=result.data)
		return JsonResponse({get_redirect_url_prop(): get_redirect_url(request)})

	redirect_url = get_redirect_url(request)
	return render_to_response(template, {get_redirect_url_prop(): redirect_url}, context_instance=RequestContext(request))


@login_required
def logout_user(request):
	"""
	Controller to logout current user
	:param request: HTTP GET request
	:return: redirect to the main page
	"""
	logout(request)
	return redirect('/')