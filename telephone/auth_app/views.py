from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from telephone.auth_app.forms import AuthUserForm
from telephone.auth_app.services import get_redirect_url, get_redirect_url_prop, sing_in


def login_page(request, template):
	redirect_url = request.GET.get('next') if request.GET.get('next') else '/'
	return render_to_response(template, {get_redirect_url_prop(): redirect_url}, context_instance=RequestContext(request))


def sign_in(request):
	auth_user_form = AuthUserForm(request.POST)
	redirect_url = get_redirect_url(request)
	if auth_user_form.errors:
		return JsonResponse({'errors': auth_user_form.errors})
	return JsonResponse({get_redirect_url_prop(): redirect_url}) if sing_in(username=auth_user_form.data['username'], password=auth_user_form.data['password'], request=request) else JsonResponse({'errors': {'password': ['Invalid Username or Password']}})


@login_required
def logout_user(request):
	logout(request)
	return redirect(get_redirect_url(request))