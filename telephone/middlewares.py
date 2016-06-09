from ast import literal_eval


class RequestBodyParserMiddleware:
	"""

	"""

	def process_request(self, request):
		"""
		Add {body_data} attr to request
		:param request: HTTP request
		:return:
		"""
		try:
			data = literal_eval(request.body or '{}')
		except ValueError as e:
			data = {}

		request.__setattr__('body_data', data)
