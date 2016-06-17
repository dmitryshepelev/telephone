from django.contrib.auth import authenticate

from telephone.auth_app.errors import AuthorizeError
from telephone.service_app.services.PBXDataService import PBXDataService


def auth(username, password):
	"""
	Authenticate and Sign in user by login and password
	:param username:
	:param password:
	:return: True if the user was singed in
	"""
	auth_user = authenticate(username = username, password = password)
	if auth_user is not None:

		# if not auth_user.is_superuser and (not auth_user.last_login or not auth_user.userprofile.sip):
		# 	auth_user.userprofile.sip = PBXDataService.get_pbx_sip(auth_user)
		# 	auth_user.userprofile.save()

		return auth_user

	raise AuthorizeError()
