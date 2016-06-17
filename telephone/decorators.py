from ast import literal_eval
from functools import wraps

from django.utils.decorators import available_attrs

from telephone.libs.ServerResponse import ServerResponse


def api_authorized():
	"""
	Decorator to make a method only accept authorized request methods. Usage::

		@api_authorized()
		def my_view(request):
			# ...

	"""
	def decorator(func):
		@wraps(func, assigned=available_attrs(func))
		def inner(request, *args, **kwargs):
			if not request.user.is_authenticated():
				return ServerResponse.unauthorized()
			return func(request, *args, **kwargs)
		return inner
	return decorator


def parse_request_body():
	"""
	Decorator to make a method only accept authorized request methods. Usage::

		@api_authorized()
		def my_view(request):
			# ...

	"""
	def decorator(func):
		@wraps(func, assigned=available_attrs(func))
		def inner(request, *args, **kwargs):
			try:
				data = literal_eval(request.body or '{}')
			except ValueError as e:
				data = {}
			request.__setattr__('body_data', data)
			return func(request, *args, **kwargs)
		return inner
	return decorator
