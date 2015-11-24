class PendingPRTransactionVM():
	def __init__(self, transaction):
		self.__transact_id = transaction.transact_id
		self.__creation_date = transaction.creation_date
		self.__email = transaction.email
		self.__username = transaction.username

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

	@property
	def username(self):
		"""
		Getter of __username
		:return: username value
		"""
		return self.__username


class HistoryPRTransactionVM(PendingPRTransactionVM):
	def __init__(self, transaction):
		PendingPRTransactionVM.__init__(self, transaction)
		self.__status_id = transaction.status_id
		self.__status_value = transaction.status.value

	@property
	def status_id(self):
		"""
		Getter of __status_id
		:return: status_id value
		"""
		return self.__status_id

	@property
	def status_value(self):
		"""
		Getter of __status_value
		:return: status_value value
		"""
		return self.__status_value