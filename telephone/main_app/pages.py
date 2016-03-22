from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@require_http_methods(['GET'])
@login_required
def base(request):
	"""
	Base of sett module
	:param request: http request
	:return: HttpResponse
	"""
	return render(request, 'page_base.html', {})


@require_http_methods(['GET'])
@login_required
def ui_view(request):
	"""
	UiView of my module
	:param request: http request
	:return: HttpResponse
	"""
	return render(request, 'ui_view.html', {})


@login_required
@user_passes_test(lambda user: not user.is_superuser)
def st_page(request):
	"""
	Page of general statistic
	:param request: http request
	:return: HttpResponse
	"""
	return render(request, 'st_page.html', {})


@login_required
@user_passes_test(lambda user: not user.is_superuser)
def check_cost_page(request):
	"""
	Page of general statistic
	:param request: http request
	:return: HttpResponse
	"""
	return render(request, 'check_cost_page.html', {})


@login_required
@user_passes_test(lambda user: not user.is_superuser)
def callback_page(request):
	"""
	Page of general statistic
	:param request: http request
	:return: HttpResponse
	"""
	return render(request, 'callback_page.html', {})


@login_required
@user_passes_test(lambda user: not user.is_superuser)
def balance_page(request):
	"""
	Page of general statistic
	:param request: http request
	:return: HttpResponse
	"""
	return render(request, 'subfee_page.html', {})


@login_required
@user_passes_test(lambda user: not user.is_superuser)
def subfee_page(request):
	"""
	Page of general statistic
	:param request: http request
	:return: HttpResponse
	"""
	return render(request, 'balance_page.html', {})