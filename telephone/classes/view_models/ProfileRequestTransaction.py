import inspect
from telephone.classes.TransactAction import TransactAction
from telephone.service_app.services.LogService import LogService, Code


class ProfileRequestTransactionVM(TransactAction):
	def __init__(self, transact):
		self.__transact = transact
		self.__logger = LogService()

	def cancel(self, **kwargs):
		"""
		Change transact status to cancel
		:return: transact
		"""
		self.__transact.status_id = 3
		return self.__save()

	def confirm(self, **kwargs):
		"""
		Execute confirm transaction
		:return: transact
		"""
		pass

	def archive(self, **kwargs):
		"""
		Archive method isn't support by profileRequestTransaction model
		:param kwargs:
		"""
		raise NotImplementedError('This method isn\'t implemented')

	def __save(self, on_success=None):
		"""
		Save entity changes
		:param on_success: callback on successful changes
		:return: True if saving executed success or False if exception has been raised
		"""
		try:
			self.__transact.save()
			if on_success and hasattr(on_success, '__call__'):
				on_success(self.__transact)
			return True
		except Exception as e:
			self.__logger.error(Code.SAVE_ENTITY_ERR, action=inspect.stack()[1][3], transact_id=self.__transact.transact_id, message=str(e))
			return False

	@property
	def transact_id(self):
		"""
		Getter of __transact_id
		:return: transact_id value
		"""
		return self.__transact.transact_id

	@property
	def creation_date(self):
		"""
		Getter of __creation_date
		:return: creation_date value
		"""
		return self.__transact.creation_date

	@property
	def email(self):
		"""
		Getter of __email
		:return: email value
		"""
		return self.__transact.email

	@property
	def username(self):
		"""
		Getter of __username
		:return: username value
		"""
		return self.__transact.username

	@property
	def status_id(self):
		"""
		Getter of __status_id
		:return: status_id value
		"""
		return self.__transact.status_id

	@property
	def status_value(self):
		"""
		Getter of __status_value
		:return: status_value value
		"""
		return self.__transact.status.value