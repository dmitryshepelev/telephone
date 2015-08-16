import logging
from django.contrib.auth.models import AnonymousUser


class AppLogger:
	def __init__(self, logger_name):
		self.logger = logging.getLogger(logger_name)

	def __get_message_string(self, message, path, request, add_data):
		path = 'Path: %s' % (path,)
		get_params_string = 'GET: %s' % (''.join('{}={}&'.format(key, value) for key, value in request.GET.items()) if request.GET else 'Empty ')
		post_params = 'POST: %s' % (''.join('{}: {}; '.format(key, value) for key, value in request.POST.items()) if request.POST else 'Empty ')
		user = 'Usercode: %s' % (request.user.userprofile.user_code if not isinstance(request.user, AnonymousUser) else 'anonymous')
		a_d = 'Data: %s' % (''.join('\n\t\t{}: {}; '.format(key, value) for key, value in add_data.items()) if add_data else '')
		return '%s\n\t%s\n\t%s\n\t%s\n\t%s\n\t%s' % (message, path, get_params_string[:-1], post_params[:-1], user, a_d)

	def debug(self, message, path, request, add_data):
		self.logger.debug(self.__get_message_string(message, path, request, add_data))

	def info(self, message, path, request, add_data):
		self.logger.info(self.__get_message_string(message, path, request, add_data))

	def warning(self, message, path, request, add_data):
		self.logger.warning(self.__get_message_string(message, path, request, add_data))

	def error(self, message, path, request, add_data):
		self.logger.error(self.__get_message_string(message, path, request, add_data))

	def critical(self, message, path, request, add_data):
		self.logger.critical(self.__get_message_string(message, path, request, add_data))