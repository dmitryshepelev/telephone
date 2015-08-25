class ApiErrorException(Exception):
	def __init__(self, api_response):
		self.message = 'Api error'
		self.url = api_response.url
		self.status_code = api_response.status_code
		self.data = api_response.content