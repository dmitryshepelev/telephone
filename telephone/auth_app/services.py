from django.contrib.auth import authenticate, login

from telephone import settings
from telephone.services import AppLogger


__logger = AppLogger('auth_logger')


def get_logger():
	return __logger


def sing_in(username, password, request):
	"""
	Authenticate and Sign in user by login and password
	:param username: username, string
	:param password: password, string
	:param request: HTTP request
	:return: True if the user was singed in
	"""
	auth_user = authenticate(username=username, password=password)
	if auth_user is not None:
		login(request, auth_user)
		return True
	get_logger().error('Error user login', request.path, request, {'Username': username, 'Password': password})
	return False


def get_redirect_url_prop():
	"""
	Returns name of the redirect url property
	:return: type 'string', redirect url property name
	"""
	__redirect_url_prop__ = 'redirect_url'
	return __redirect_url_prop__


def get_redirect_url(request):
	"""
	Returns redirect URL string after GET or POST request.
	Redirect to the Main page if redirect URL is undefined.
	:param request: HTTP request
	:return: URL string
	"""
	if request.method == 'GET':
		return request.GET.get('next') if request.GET.get('next') else settings.SCHEMA_URL
	return request.POST.get(get_redirect_url_prop())
