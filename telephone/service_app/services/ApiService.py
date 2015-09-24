import json
import requests
import datetime
from telephone import settings
from telephone.classes.ServiceResponse import ServiceResponse


class ApiService():
	def __init__(self):
		pass

	@staticmethod
	def get_url(reason):
		"""
		Returns url to the api depending on reason
		:param reason: string
		:return: ServiceResponse
		"""
		result = ''
		status = True
		if reason == 'OAuthCode':
			result = '%s%s&client_id=%s' % (settings.API_URLS['oauth']['host'], settings.API_URLS['oauth']['authorize'], settings.O_AUTH_ID)
		else:
			status = not status
		return ServiceResponse(status, result)

	@staticmethod
	def get_token(code):
		"""
		Get OAuth token to api access
		Api response data: {'access_token': 'token', 'token_type': 'bearer', 'expires_in': 'time_in_seconds'}
		:param code: verifying code
		:return: ServiceResponse
		"""
		request_string = '%s%s' % (settings.API_URLS['oauth']['host'], settings.API_URLS['oauth']['token'])
		api_response = requests.post(request_string, {'grant_type': 'authorization_code', 'code': code, 'client_id': settings.O_AUTH_ID, 'client_secret': settings.O_AUTH_SECRET}, headers={'Content-type': 'application/x-www-form-urlencoded'})
		return ServiceResponse(api_response.ok, api_response.content)

	@staticmethod
	def generate_email_password(email_id):
		"""
		Generate password based on template: 'wt[day][month][year]$[login]
		:param email_id: user's login
		:return: string password
		"""
		return 'wt%s$%s' % (datetime.datetime.now().strftime('%d%m%y'), email_id)

	@staticmethod
	def create_domain_mail(params):
		"""
		Create new domain email.
		:param params: MailParameters instance
		:return: ServiceResponse, api response data: {'domain': 'name', 'login': 'email', 'uid': 'uid, 'success': 'status'}
		"""
		request_string = '%s%s' % (settings.API_URLS['mail']['host'], settings.API_URLS['mail']['create_mail'])
		api_response = requests.post(request_string, params.get_params(), headers={'PddToken': settings.MAIL_A_TOKEN})
		return ServiceResponse(api_response.ok, json.loads(api_response.content))