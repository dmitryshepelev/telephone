from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, JsonResponse

from telephone.service_app.services.api_service import ApiService


@login_required
@user_passes_test(lambda user: user.is_superuser)
def get_api_urls(request):
	"""
	Api access url based on 'reason' GET parameter
	:param request: HTTP request
	:return: dict
	"""
	if request.GET:
		return JsonResponse(ApiService.get_url(request.GET.get('reason'))) or HttpResponse(status=500)


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
			return JsonResponse(result.data) if result.status else HttpResponse(status=500)