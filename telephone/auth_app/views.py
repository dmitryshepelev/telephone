from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext
from django.views.decorators.http import require_http_methods

from telephone.classes.ProfileRequest import ProfileRequest
from telephone.service_app.services.CommonService import CommonService
from telephone.service_app.services.DBService import DBService
from telephone.service_app.services.LocalizeService import LocalizeService
from telephone.service_app.services.LogService import LogService, Code


logger = LogService()


# def login(request, template):
# 	"""
# 	Controller to show login page
# 	:param request: HTTP GET request
# 	:param template: html template
# 	:return: HttpResponse
# 	"""
# 	redirect_property_name = 'redirect_url'
# 	if request.method == 'POST':
# 		result = AuthService().sign_in(request)
# 		if not result.is_success:
# 			data = [{key: LocalizeService(value[0]).get_localized_value()} for key, value in result.data.iteritems()]
# 			logger.warning(Code.INVLOG, data=data, POST=request.POST, path=request.path)
# 			return JsonResponse(CommonService.parse_form_errors(data), status=400)
# 		redirect_url = request.POST.get(redirect_property_name)
# 		return JsonResponse({redirect_property_name: redirect_url})
#
# 	redirect_url = request.GET.get('next') if request.GET.get('next') else '/'
# 	return render_to_response(template, {redirect_property_name: redirect_url}, context_instance=RequestContext(request))


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


# @require_http_methods(['POST'])
# def new_profile_request(request, template):
# 	"""
# 	Controller to create new profile request
# 	:param request: HTTP request
# 	:param template: html template
# 	:return: HttpResponse
# 	"""
# 	profile_request_transact = DBService.create_profile_request_transact(ProfileRequest(request.POST.get('email'), request.POST.get('login')))
# 	if profile_request_transact:
# 		return render_to_response(template, {'email': profile_request_transact.email, 'transact_id': profile_request_transact.transact_id}, context_instance=RequestContext(request))
#
# 	return HttpResponse(status=500)
#
#
@login_required
def logout_user(request):
	"""
	Controller to logout current user
	:param request: HTTP GET request
	:return: redirect to the main page
	"""
	logout(request)
	return redirect('/auth/login/')
