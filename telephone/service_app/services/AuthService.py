# coding=utf-8
from django.contrib.auth import authenticate, login

from telephone.classes.forms.AuthUserForm import AuthUserForm
from telephone.classes.ServiceResponse import ServiceResponse


class AuthService():
	def __init__(self):
		pass

	@staticmethod
	def sign_in(request):
		"""
		Authenticate and Sign in user by login and password
		:param request: HTTP request
		:return: True if the user was singed in
		"""
		form = AuthUserForm(request.POST)
		if form.errors:
			return ServiceResponse(False, form.errors)
		auth_user = authenticate(username=form.data['username'], password=form.data['password'])
		if auth_user is not None:
			login(request, auth_user)
			return ServiceResponse(True)
		return ServiceResponse(False, {'username': ['Invalidusernameorpassword'], 'password': ['Invalidusernameorpassword']})