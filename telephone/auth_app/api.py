# coding=utf-8
from django.contrib.auth import login as log
from django.views.decorators.http import require_http_methods

from telephone.auth_app.errors import AuthorizeError
from telephone.auth_app.forms import AuthUserForm, ProfileRequestForm
from telephone.auth_app.services import auth
from telephone.classes.Message import Message
from telephone.classes.ProfileRequest import ProfileRequest
from telephone.service_app.services.DBService import DBService


@require_http_methods(['POST'])
def login(request):
	"""
	Controller to show login page
	:param request: HTTP GET request
	:return: HttpResponse
	"""
	from telephone.classes.ServerResponse import ServerResponse

	redirect_property_name = 'redirect_url'

	form = AuthUserForm(request.body_data)

	if form.errors:
		return ServerResponse.bad_request(data = form.errors)

	try:
		auth_user = auth(request.body_data.get('username'), request.body_data.get('password'))
		log(request, auth_user)

	except AuthorizeError as e:
		return ServerResponse.bad_request(message = Message.error(e.message))

	redirect_url = request.POST.get(redirect_property_name)
	return ServerResponse.ok(data = {redirect_property_name: redirect_url or '/'})


@require_http_methods(['POST'])
def profile_request(request):
	"""
	Controller to create profile request
	:param request:
	:return:
	"""
	from telephone.classes.ServerResponse import ServerResponse

	form = ProfileRequestForm(request.body_data)

	if form.errors:
		return ServerResponse.bad_request(form.errors)

	profile_request_transact = DBService.create_profile_request_transact(ProfileRequest(request.body_data.get('email'), request.body_data.get('login')))

	if profile_request_transact:
		return ServerResponse.ok(data = {'transact_id': profile_request_transact.transact_id, 'email': profile_request_transact.email},
		                         message = Message.success('Заявка успешно создана'))

	return ServerResponse.internal_server_error()
