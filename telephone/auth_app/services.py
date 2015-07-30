from django.contrib.auth import authenticate, login
from telephone.auth_app.forms import AuthUserForm


def sing_in(username, password, request):
	"""
		Authenticate and Sign in user by login and password
	:param username: username, string
	:param password: password, string
	:param request: HTTP request
	:return: True if the user was singed in
	"""
	user = authenticate(username=username, password=password)
	if user is not None:
		login(request, user)
		return True
	return False


def get_redirect_url_prop():
	__redirect_url_prop__ = 'redirect_url'
	return __redirect_url_prop__


def get_redirect_url(request):
	"""
		Returns redirect URL string after GET or POST requests.
		Redirect to the Main page if redirect URL is undefined.
	:param request: HTTP request
	:return: URL string
	"""
	if request.method == 'GET':
		return request.GET.get('next') if request.GET.get('next') else '/'
	return request.POST.get(get_redirect_url_prop())