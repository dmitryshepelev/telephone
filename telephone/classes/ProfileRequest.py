import datetime
import uuid


class ProfileRequest():
	def __init__(self, email, login=None):
		self.__transact_id = str(uuid.uuid4())
		self.__creation_date = datetime.datetime.now()
		self.__email = email
		self.__login = login

	@property
	def transact_id(self):
		"""
		Getter of __transact_id
		:return: transact_id value
		"""
		return self.__transact_id

	@property
	def creation_date(self):
		"""
		Getter of __creation_date
		:return: creation_date value
		"""
		return self.__creation_date

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