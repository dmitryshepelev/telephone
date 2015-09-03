import requests
from telephone import settings


class _ApiResponse():
	def __init__(self, status, data):
		self.status = status
		self.data = data or None


class ApiService():
	def __init__(self):
		pass

	@staticmethod
	def get_url(reason):
		"""
		Returns url to the api depending on reason
		:param reason: string
		:return: object {'url' <value>}
		"""
		result = {}
		if reason == 'OAuthCode':
			result['url'] = '%s%s&client_id=%s' % (settings.API_URLS['oauth']['host'], settings.API_URLS['oauth']['authorize'], settings.O_AUTH_ID)
		return result

	@staticmethod
	def get_token(code):
		"""
		Get OAuth token to api access
		:param code: verifying code
		:return: api response data: {'access_token': 'token', 'token_type': 'bearer', 'expires_in': 'time_in_seconds'}
		"""
		request_string = '%s%s' % (settings.API_URLS['oauth']['host'], settings.API_URLS['oauth']['token'])
		api_response = requests.post(request_string, {'grant_type': 'authorization_code', 'code': code, 'client_id': settings.O_AUTH_ID, 'client_secret': settings.O_AUTH_SECRET}, headers={'Content-type': 'application/x-www-form-urlencoded'})
		return _ApiResponse(api_response.ok, api_response.content)