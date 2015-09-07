from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from telephone import settings

from telephone.classes.forms.NewUserForm import NewUserForm
from telephone.service_app.services.ApiService import ApiService
from telephone.service_app.services.CommonService import CommonService
from telephone.service_app.services.ProfileService import ProfileService


@login_required
@user_passes_test(lambda user: user.is_superuser)
def create_new_user(request, template):
	"""
	Create new user controller
	:param request: HTTP request
	:param template: html template
	:return:
	"""
	if request.POST:
		new_user_form = NewUserForm(request.POST)
		if new_user_form.errors:
			return JsonResponse({'isSuccess': False, 'data': new_user_form.errors})
		result = ProfileService.create_profile(new_user_form.data)
		if result.is_success:
			return HttpResponse(status=201, content={'isSuccess': True})
		return HttpResponse(status=500)
	else:
		email_id = CommonService.get_random_string(6, only_digits=True)
		response_params = {'email_id': email_id, 'password': ApiService.generate_email_password(email_id), 'domain': '@%s' % settings.DOMAIN}
		return render_to_response(template, response_params, context_instance=RequestContext(request))