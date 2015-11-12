# coding=utf-8
class PendingTransactionVM():
	def __init__(self, transaction):
		self.__transact_id = transaction.transact_id
		self.__sum = transaction.sum
		self.__payment_type = transaction.payment_type
		self.__duration = transaction.duration
		self.__username = transaction.user_profile.user.username
		self.__creation_date = transaction.creation_date

	@property
	def transact_id(self):
		"""
		Getter of __transact_id
		:return: transact_id value
		"""
		return self.__transact_id

	@property
	def sum(self):
		"""
		Getter of __sum
		:return: sum value
		"""
		return self.__sum

	@property
	def payment_type(self):
		"""
		Getter of __payment_type
		:return: payment_type value
		"""
		return self.__payment_type

	@property
	def duration(self):
		"""
		Getter of __duration
		:return: duration value
		"""
		return '{value} мес'.format(value=self.__duration)

	@property
	def username(self):
		"""
		Getter of __username
		:return: username value
		"""
		return self.__username

	@property
	def creation_date(self):
		"""
		Getter of __creation_date
		:return: creation_date value
		"""
		return self.__creation_date


class ArchiveTransactionVM(PendingTransactionVM):
	def __init__(self, transaction):
		PendingTransactionVM.__init__(self, transaction)
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


class HistoryTransactionVM(ArchiveTransactionVM):
	def __init__(self, transaction):
		ArchiveTransactionVM.__init__(self, transaction)
		self.__is_archive = transaction.is_archive

	@property
	def is_archive(self):
		"""
		Getter of __is_archive
		:return: is_archive value
		"""
		return self.__is_archive