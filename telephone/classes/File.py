class File():
	def __init__(self, stream, filename=None):
		self.__stream = stream
		self.__filename = filename

	@property
	def content(self):
		"""
		Getter of __stream
		:return: stream
		"""
		return self.__stream

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