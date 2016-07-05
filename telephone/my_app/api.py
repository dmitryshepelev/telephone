from django.utils import timezone
from django.views.decorators.http import require_http_methods

from telephone.decorators import api_authorized
from telephone.libs.ServerResponse import ServerResponse
from telephone.my_app.services.PBXService import PBXService, StatParams
from telephone.my_app.utils import DateTimeUtil


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


@require_http_methods(['GET'])
@api_authorized()
def get_stat(request):
	"""
	Returns stats
	:param request:
	:return:
	"""
	user = request.user
	stat_params = StatParams(
		start = DateTimeUtil.from_timestamp(request.GET.get('start', DateTimeUtil.to_timestamp(timezone.now()))),
		end = DateTimeUtil.from_timestamp(request.GET.get('end', DateTimeUtil.to_timestamp(timezone.now()))),
		status = request.GET.get('status', 0),
		call_type = request.GET.get('call_type', ''),
	)

	service = PBXService(user.pbx)
	service.update_stat(stat_params)

	calls = user.pbx.pbxcall_set.filter(date__gte = stat_params.start, date__lte = stat_params.end)

	return ServerResponse.ok(data = {'calls': [call.serialize() for call in calls]})
