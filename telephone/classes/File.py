class File():
	def __init__(self, stream=None, filename=None, path=None):
		self.__stream = stream
		self.__filename = filename
		self.__path = path

	@property
	def content(self):
		"""
		Getter of __stream
		:return: stream
		"""
		return self.__stream

	@content.setter
	def content(self, value):
		"""
		Setter of __content
		:param value: value to set
		"""
		self.__stream = value

	@property
	def filename(self):
		"""
		Getter of __filename
		:return: filename
		"""
		return self.__filename

	@filename.setter
	def filename(self, value):
		"""
		Setter of __filename
		:param value: value to set
		"""
		if len(value) > 1000:
			raise ValueError

		self.__filename = value

	@property
	def path(self):
		"""
		Getter of __path
		:return: path
		"""
		return self.__path

	@path.setter
	def path(self, value):
		"""
		Setter of __path
		:param value: value to set
		"""
		self.__path = value