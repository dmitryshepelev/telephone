from django.views.decorators.http import require_http_methods

from telephone.decorators import api_authorized
from telephone.libs.ServerResponse import ServerResponse


@require_http_methods(['GET'])
@api_authorized()
def get_pbx_info(request):
	"""
	Returns PBX profile info
	:param request:
	:return:
	"""
	data = {
		'username': request.user.username,
	}
	return ServerResponse.ok(data = data)
