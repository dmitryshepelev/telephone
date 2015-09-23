class ServiceResponse():
	def __init__(self, status, data=None, message=''):
		"""
		Constructor
		:param status: response status: True - 'ok', False - 'error'
		:param data: response data
		:param message: response message
		"""
		self.__is_success = status
		self.__data = data
		self.__message = message

	@property
	def is_success(self):
		"""
		Getter of __is_success
		:return: __is_success
		"""
		return self.__is_success

	@property
	def data(self):
		"""
		Getter of __data
		:return: data
		"""
		return self.__data

	@data.setter
	def data(self, value):
		"""
		Setter og __data
		:param value: data
		:return:
		"""
		self.__data = value

	@property
	def message(self):
		"""
		Getter of __message
		:return: message
		"""
		return self.__message