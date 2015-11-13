from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from telephone.classes.forms.NewUserForm import NewUserForm
from telephone.classes.view_models.SubscribeTransaction import PendingTransactionVM, ArchiveTransactionVM, \
	HistoryTransactionVM
from telephone.main_app.models import SubscribeTransaction
from telephone.service_app.services.CommonService import CommonService
from telephone.service_app.services.LogService import LogService, Code
from telephone.service_app.services.ProfileService import ProfileService


logger = LogService()


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
		logger.error(Code.PCRERR, data=result.data)
		return HttpResponse(status=500, content=result.data)
	else:
		return render_to_response(template, {}, context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda user: user.is_superuser)
def panel(request, template):
	"""
	Controller to view admin panel
	:param request: HTTP request
	:param template: html template
	:return: HttpResponse instance
	"""
	return render_to_response(template, {}, context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda user: user.is_superuser)
def get_pending_transacts(request, template):
	"""
	Controller to get pending transacts partial
	:param request: HTTP request
	:param template: html template
	:return: HttpResponse instance
	"""
	pending_transact = [PendingTransactionVM(transact) for transact in SubscribeTransaction.objects.filter(status_id=1, is_archive=False).order_by('-creation_date')]
	return render_to_response(template, {'pending_transact': pending_transact}, context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda user: user.is_superuser)
def get_archive_transacts(request, template):
	"""
	Controller to get pending transacts partial
	:param request: HTTP request
	:param template: html template
	:return: HttpResponse instance
	"""
	CommonService.send_mail()
	transacts = [ArchiveTransactionVM(transact) for transact in SubscribeTransaction.objects.filter(is_archive=True).order_by('-creation_date')]
	return render_to_response(template, {'transacts': transacts}, context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda user: user.is_superuser)
def get_history_transacts(request, template):
	"""
	Controller to get pending transacts partial
	:param request: HTTP request
	:param template: html template
	:return: HttpResponse instance
	"""
	transacts = [HistoryTransactionVM(transact) for transact in SubscribeTransaction.objects.filter().order_by('-creation_date')]
	return render_to_response(template, {'transacts': transacts}, context_instance=RequestContext(request))