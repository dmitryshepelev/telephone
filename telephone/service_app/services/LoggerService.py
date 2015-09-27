import logging
from enum import Enum

__logger = logging.getLogger('app_logger')


class Code(Enum):
	pass


class LoggerService():
	def __init__(self):
		self.__logger = logging.getLogger('app_logger')
		self.__template = '{code} {message}\n{data}'

	def __get_log_text(self, code, message, data):
		return self.__template.format(code=code, message=message, data=self.format_data(data))

	def error(self, code, message=None, data=None):
		self.__logger.error(self.__get_log_text(code, message, data))

	def format_data(self, data, iteration=0):
		template = '{newline}{key}: {value}\n'
		formatted_data = ''
		if isinstance(data, dict):
			formatted_data += '\n' if iteration > 0 else ''
			for key, value in data.items():
				formatted_data += template.format(key=key, newline=''.join(['    '] * iteration), value=self.format_data(value, iteration + 1))
		elif type(data) is str:
			return data
		return formatted_data