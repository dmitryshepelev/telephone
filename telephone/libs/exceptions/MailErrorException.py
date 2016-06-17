class MailErrorException(Exception):
	def __init__(self, api_response=None, response_content=None):
		self.message = 'Mail creation error'
		if api_response:
			self.url = api_response.url
			self.status_code = api_response.status_code
		if response_content:
			self.domain = response_content['domain']
			self.success = response_content['success']
			self.error = response_content['error']
