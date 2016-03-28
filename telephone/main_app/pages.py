from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from telephone.classes.PaymentData import PaymentData
from telephone.classes.SubscriptionData import SubscriptionData


@require_http_methods(['GET'])
@login_required
def base(request, template):
	"""
	Base of sett module
	:param request: http request
	:return: HttpResponse
	"""
	return render(request, template, {})


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
	return render(request, 'balance_page.html', {'payment_data': PaymentData(request.user.userprofile.customer_number)})


@login_required
@user_passes_test(lambda user: not user.is_superuser)
def subfee_page(request):
	"""
	Page of general statistic
	:param request: http request
	:return: HttpResponse
	"""
	return render(request, 'subfee_page.html', {'subscription_data': SubscriptionData()})


@login_required
def get_widget_script_page(request):
	"""
	Return widget script
	:param request:
	:return:
	"""
	return render(request, 'get_widget_script_page.html', {})