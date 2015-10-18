import inspect
import logging
from enum import Enum

__logger = logging.getLogger('app_logger')


class Code(Enum):
	INVLOG = 'INVLOG Invalid logging data'

	PCRERR = 'PCRERR Profile creation error'
	GTKERR = 'GTKERR Get token error'
	MCRERR = 'MCRERR Mail creation error'

	UCLEXE = 'UCLEXE Update calls list executed succeed'
	UCLNTU = 'UCLNTU Nothing to update'
	UCLSWE = 'UCLSWE Succeed with errors'
	UCLUNS = 'UCLUNS Unsucceed'


class LogService():
	def __init__(self):
		self.__logger = logging.getLogger('app_logger')
		self.__template = '[{callee}] {code}\n{data}'

	def __get_log_text(self, code, callee, data):
		return self.__template.format(callee=callee, code=code, data=self.__format_data(data))

	def error(self, code, **data):
		self.__logger.error(self.__get_log_text(code, inspect.stack()[1][3], data))

	def warning(self, code, **data):
		self.__logger.warning(self.__get_log_text(code, inspect.stack()[1][3], data))

	def info(self, code, **data):
		self.__logger.info(self.__get_log_text(code, inspect.stack()[1][3], data))

	def __format_data(self, data, iteration=0):
		template = '{space}{key}: {value}\n'
		formatted_data = ''
		if isinstance(data, dict):
			formatted_data += '\n' if iteration > 0 else ''
			for key, value in data.items():
				formatted_data += template.format(key=key, space=''.join(['  ' * iteration]), value=self.__format_data(value, iteration + 1))
		elif type(data) is str or type(data) is int or type(data) is bool:
			return data
		elif type(data) is unicode:
			return data.encode()
		elif isinstance(data, list) or type(data) is tuple:
			for d in data:
				formatted_data += self.__format_data(d, iteration + 1)
		elif isinstance(data, Code):
			return data.value
		return formatted_data