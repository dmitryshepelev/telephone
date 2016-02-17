# coding=utf-8
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.views.decorators.http import require_http_methods

from telephone.classes.MailParameters import MailParameters
from telephone.classes.Modals import Modal
from telephone.classes.search_models.ProfileRequestTransactionSM import ProfileRequestTransactionSM
from telephone.classes.search_models.ProfileSM import ProfileSM
from telephone.classes.search_models.SubscribeTransactionSM import SubscribeTransactionSM
from telephone.main_app.models import SubscribeTransaction, ProfileRequestTransaction
from telephone.service_app.services.CommonService import CommonService
from telephone.service_app.services.ApiService import ApiService
from telephone.service_app.services.DBService import DBService
from telephone.service_app.services.LogService import LogService, Code
from telephone.shared_views import default_404


logger = LogService()


@login_required
@user_passes_test(lambda user: user.is_superuser)
def get_api_urls(request):
	"""
	Api access url based on 'reason' GET parameter
	:param request: HTTP request
	:return: dict
	"""
	if request.GET:
		result = ApiService.get_url(request.GET.get('reason'))
		if result.is_success:
			return JsonResponse({'url': result.data})
	return HttpResponse(status=500)


@login_required
@user_passes_test(lambda user: user.is_superuser)
def get_oauth_token(request):
	"""
	Get OAuth token to api access
	:param request: HTTP request
	:return: dict
	"""
	if request.POST:
		code = request.POST.get('code')
		if code:
			result = ApiService.get_token(code)
			status_code = 200
			if not result.is_success:
				status_code = 400
				logger.error(Code.GTKERR, data=result.data, POST=request.POST)
			return JsonResponse(result.data, status=status_code)
	return HttpResponse(status=500)


@login_required
@user_passes_test(lambda user: user.is_superuser)
def generate_password(request):
	"""
	Generate random password
	:param request: HTTP request
	:return: dict with 'password' key
	"""
	return JsonResponse({'password': CommonService.get_random_string(10)})


@login_required
def get_transact_id(request):
	"""
	Get transact id
	:param request: HTTP request
	:return: guid
	"""
	return JsonResponse({'id': CommonService.get_guid()})


@login_required
@user_passes_test(lambda user: user.is_superuser)
@require_http_methods(['POST'])
def create_mail(request):
	"""
	Creates new email
	:param request: HTTP request
	:return: JsonResponse
	"""
	if request.POST:
		params = MailParameters(request.POST)
		result = ApiService.create_domain_mail(params)
		if result.is_success and result.data['success'] == 'ok':
			update_result = ApiService.update_mailbox_params(result.data['login'])
			if update_result.is_success:
				return JsonResponse({'login': result.data['login'], 'uid': result.data['uid']})
		logger.error(Code.MCRERR, data=result.data, POST=request.POST)
		return JsonResponse(result.data, status=400)
	return HttpResponse(status=500)


@login_required
@user_passes_test(lambda user: user.is_superuser)
def get_mailbox_data(request):
	"""
	Controller to get new mailbox data
	:param request: HTTP request
	:return: JsonResponse
	"""
	return JsonResponse(ApiService.generate_mailbox_data().data)


@login_required
@user_passes_test(lambda user: user.is_superuser)
@require_http_methods(['POST'])
def transact_action(request, action):
	"""
	Controller to execute transact action
	:param request: HTTP request
	:return: JsonResponse instance
	"""
	transact_id = request.POST.get('transactId')

	transact = DBService.get_transact(transact_id)
	if not transact:
		return HttpResponse(status=500)

	result = transact.__getattribute__(action)(request=request)
	if result:
		return JsonResponse({'transactId': transact.transact_id})

	return HttpResponse(status=500)


@login_required
@require_http_methods(['GET'])
@user_passes_test(lambda user: user.is_superuser)
def search(request):
	"""
	Controller to return search result
	:param request: HTTP request
	:return: JsonResponse
	"""
	query = request.GET.get('q')
	target = request.GET.get('target')

	if request.user.is_superuser and query:
		search_result = {}

		search_result['scrb_transacts'] = [SubscribeTransactionSM(transact).model for transact in SubscribeTransaction.objects.filter(transact_id__icontains=query).order_by('-creation_date')[:3]]
		search_result['pr_transacts'] = [ProfileRequestTransactionSM(transact).model for transact in ProfileRequestTransaction.objects.filter(transact_id__icontains=query).order_by('-creation_date')[:3]]
		search_result['profiles'] = [ProfileSM(profile).model for profile in User.objects.filter(Q(username__icontains=query) | Q(email__icontains=query))[:3]]

		return JsonResponse(search_result)

	return HttpResponse(status=500)


@login_required
@require_http_methods(['GET'])
@user_passes_test(lambda user: user.is_superuser)
def element(request, type, id):
	"""
	Controller to get element page
	:param request: HTTP request
	:param type: element type
	:param id: element id
	:return:
	"""
	if type == 'scrb' or type == 'pr':

		transact = DBService.get_transact(id)

		if not transact:
			return default_404(request)

		as_partial = bool(request.GET.get('as_partial', False))
		return render_to_response('transact_element_partial.html' if as_partial else 'element_base.html', {'transact': transact, 'type': type}, context_instance=RequestContext(request))
	elif type == 'profile':

		try:
			profile = User.objects.get(email=id)
		except ObjectDoesNotExist as e:
			return default_404(request)

		return render_to_response('profile.html', {'profile': profile}, context_instance=RequestContext(request))
	return HttpResponse(status=200)


@login_required
@require_http_methods(['GET'])
def get_modal(request, modal):
	"""
	Get modal content partial page
	:param request: http request
	:param modal: modal name
	:return:
	"""
	modal = Modal.factory(modal, request.GET)
	return render_to_response(modal.template, modal.params, context_instance=RequestContext(request))


@require_http_methods(['GET'])
def get_widget_modal(request):
	"""
	returns widget modal template
	:param request:
	:return:
	"""
	modal = Modal.factory('widget', {})

	content = loader.render_to_string(modal.template, modal.params)
	response = HttpResponse(status=200)
	response['Access-Control-Allow-Origin'] = '*'
	response.content = content

	return response

