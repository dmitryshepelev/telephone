class ProfileRequest():
	def __init__(self, email, login=None):
		self.__email = email
		self.__login = login

	@property
	def email(self):
		"""
		Getter of __email
		:return: email value
		"""
		return self.__email

	@email.setter
	def email(self, value):
		"""
		Setter of __email
		:param value: value to set
		"""
		self.__email = value

	@property
	def login(self):
		"""
		Getter of __login
		:return: login value
		"""
		return self.__login

	@login.setter
	def login(self, value):
		"""
		Setter of __login
		:param value: value to set
		"""
		self.__login = value