from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from telephone.service_app.services.LogService import LogService


def base(request):
	"""
	Base template
	:param request:
	:return:
	"""
	redirect_url = request.GET.get('next', '')
	return render(request, 'auth_base.html', {'redirect_url': redirect_url})


def ui_view(request):
	"""
	Ui-view
	:param request:
	:return:
	"""
	return render(request, 'auth_ui_view.html', {})


def login_page(request):
	"""
	Returns login page template
	:param request:
	:return:
	"""
	return render(request, 'login_page.html', {})


@login_required
def logout_user(request):
	"""
	Controller to logout current user
	:param request: HTTP GET request
	:return: redirect to the main page
	"""
	logout(request)
	return redirect('/auth/login/')
