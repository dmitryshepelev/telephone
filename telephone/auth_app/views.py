import logging

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from telephone.service_app.services.AuthService import AuthService
from telephone.service_app.services.CommonService import CommonService
from telephone.service_app.services.LocalizeService import LocalizeService


logger = logging.getLogger('auth_logger')


def login(request, template):
	"""
	Controller to show login page
	:param request: HTTP GET request
	:param template: html template
	:return: HttpResponse
	"""
	redirect_property_name = 'redirect_url'
	if request.method == 'POST':
		result = AuthService().sign_in(request)
		if not result.is_success:
			data = [{key: LocalizeService(value[0]).get_localized_value()} for key, value in result.data.iteritems()]
			LoggerService.error()
			return JsonResponse(CommonService.parse_form_errors(data), status=400)
		return JsonResponse({redirect_property_name: request.POST.get(redirect_property_name)})

	redirect_url = request.GET.get('next') if request.GET.get('next') else '/calls/'
	return render_to_response(template, {redirect_property_name: redirect_url}, context_instance=RequestContext(request))


@login_required
def logout_user(request):
	"""
	Controller to logout current user
	:param request: HTTP GET request
	:return: redirect to the main page
	"""
	logout(request)
	return redirect('/')