from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from telephone.auth_app.forms import AuthUserForm
from telephone.auth_app.services import get_redirect_url, get_redirect_url_prop, sing_in


def login_page(request, template):
	"""
	Controller to show login page
	:param request: HTTP GET request
	:param template: html template
	:return: HttpResponse
	"""
	redirect_url = get_redirect_url(request)
	return render_to_response(template, {get_redirect_url_prop(): redirect_url}, context_instance=RequestContext(request))


def sign_in(request):
	"""
	Controller to authenticate and sign in user
	:param request: HTTP POST request
	:return: JsonResponse with the result of the authentication. Returns object with redirect url property,
	if user was signed in successfully.
	"""
	auth_user_form = AuthUserForm(request.POST)
	if auth_user_form.errors:
		return JsonResponse({'errors': auth_user_form.errors})
	if sing_in(code=auth_user_form.data['code'], password=auth_user_form.data['password'], request=request):
		return JsonResponse({get_redirect_url_prop(): get_redirect_url(request)})
	else:
		return JsonResponse({'errors': {'password': ['Invalid Username or Password']}})


@login_required
def logout_user(request):
	"""
	Controller to logout current user
	:param request: HTTP GET request
	:return: redirect to the main page
	"""
	logout(request)
	return redirect('/')