import uuid

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from telephone import settings


def main_resolver(request):
	"""
	Controller to show main page
	:param request: HTTP GET request
	:param templates: html templates
	:return: HttpResponse instance
	"""
	if request.user.is_authenticated() and request.user.is_superuser:
		# return panel(request, templates[0])
		pass
	return base(request, 'my_base.html')


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
	return render(request, 'my_ui_view.html', {})


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
	payment_data = settings.PAYMENT_DATA
	payment_data['customer_number'] = request.user.pbx.customer_number
	return render(request, 'balance_page.html', {'payment_data': payment_data})


@login_required
@user_passes_test(lambda user: not user.is_superuser)
def subfee_page(request):
	"""
	Page of general statistic
	:param request: http request
	:return: HttpResponse
	"""
	subscription_data = settings.SUBSCRIPTION_DATA
	subscription_data['label'] = str(uuid.uuid4())
	return render(request, 'subfee_page.html', {'subscription_data': subscription_data})


@login_required
def get_widget_script_page(request):
	"""
	Return widget script
	:param request:
	:return:
	"""
	return render(request, 'get_widget_script_page.html', {})