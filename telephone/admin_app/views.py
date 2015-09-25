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
			return JsonResponse({'data': new_user_form.errors}, status=400)
		result = ProfileService.create_profile(new_user_form.data)
		if result.is_success:
			return HttpResponse(status=201)
		return HttpResponse(status=500)
	else:
		return render_to_response(template, ApiService.generate_mailbox_data().data, context_instance=RequestContext(request))