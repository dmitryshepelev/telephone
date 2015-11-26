# coding=utf-8
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from telephone.classes.forms.NewUserForm import NewUserForm
from telephone.classes.view_models.ProfileRequestTransaction import ProfileRequestTransactionVM
from telephone.classes.view_models.SubscribeTransaction import SubscribeTransactionVM
from telephone.main_app.models import SubscribeTransaction, ProfileRequestTransaction
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
def get_subscribe_transacts(request, transact_type):
	"""
	Controller to get subscribe transacts partial
	:param request: HTTP request
	:return: HttpResponse instance
	"""
	order = '-creation_date'

	# TODO: refactor
	if transact_type == 'pending':
		transacts = [SubscribeTransactionVM(transact) for transact in SubscribeTransaction.objects.filter(status_id=1, is_archive=False).order_by(order)]
		template = 'pending_transacts.html'
	elif transact_type == 'archive':
		transacts = [SubscribeTransactionVM(transact) for transact in SubscribeTransaction.objects.filter(is_archive=True).order_by(order)]
		template = 'archive_transacts.html'
	elif transact_type == 'history':
		transacts = [SubscribeTransactionVM(transact) for transact in SubscribeTransaction.objects.filter().order_by(order)]
		template = 'history_transacts.html'
	else:
		return HttpResponse(status=400)

	page_number = request.GET.get('page')
	pager_data = CommonService.define_page(transacts, page_number, data_field_name='transacts')
	pager_data['transact_type'] = transact_type

	return render_to_response(template, pager_data, context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda user: user.is_superuser)
def get_pr_transacts(request, transact_type):
	"""
	Controller to get profile request transacts partial
	:param request: HTTP request
	:return: HttpResponse instance
	"""
	order = '-creation_date'

	if transact_type == 'pending':
		transacts = [ProfileRequestTransactionVM(transact) for transact in ProfileRequestTransaction.objects.filter(status_id=1).order_by(order)]
		template = 'pending_pr_transacts.html'
	elif transact_type == 'history':
		transacts = [ProfileRequestTransactionVM(transact) for transact in ProfileRequestTransaction.objects.filter().order_by(order)]
		template = 'history_pr_transacts.html'
	else:
		return HttpResponse(status=400)

	page_number = request.GET.get('page')
	pager_data = CommonService.define_page(transacts, page_number, data_field_name='transacts')
	pager_data['transact_type'] = transact_type

	return render_to_response(template, pager_data, context_instance=RequestContext(request))