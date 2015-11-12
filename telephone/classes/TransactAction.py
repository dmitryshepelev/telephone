import datetime
from telephone.main_app.models import TransactionStatus
from telephone.service_app.services.CommonService import CommonService
from telephone.service_app.services.LogService import LogService, Code


class TransactAction():
	def __init__(self, action_id):
		self.__logger = LogService()
		self.__action_id = int(action_id)
		self.__action = None

		self.__set_action(self.__action_id)

	@property
	def action_id(self):
		"""
		Getter of __action_id
		:return: action_id value
		"""
		return self.__action_id

	@action_id.setter
	def action_id(self, value):
		"""
		Setter of __action_id
		:param value: value to set
		"""
		if value is not int:
			try:
				value = int(value)
			except Exception as e:
				raise TypeError

		self.__action_id = value
		self.__set_action(self.__action_id)

	def __set_action(self, action_id):
		"""
		Set action to execute
		:param action_id: {int} action id
		"""
		if action_id == 1:
			self.__action = self.__confirm
		elif action_id == 2:
			self.__action = self.__cancel
		elif action_id == 3:
			self.__action = self.__to_archive
		elif action_id == 4:
			self.__action = self.__from_archive
		elif action_id == 0:
			self.__action = self.__pending

	def __confirm(self, transact):
		"""
		Execute confirm transaction
		:param transact: transact instance
		:return: transact
		"""
		status_id = 2

		if transact.status_id == status_id:
			return False

		status = TransactionStatus.objects.get(pk=status_id)

		transact.status = status
		transact.expiration_date = CommonService.add_months(datetime.datetime.now(), transact.duration)
		transact.save()
		return transact

	def __cancel(self, transact):
		"""
		Execute cancel transaction
		:param transact: transact instance
		:return: transact
		"""
		status_id = 3

		if transact.status_id == status_id:
			return False

		status = TransactionStatus.objects.get(pk=status_id)

		transact.status = status
		transact.save()
		return transact

	def __pending(self, transact):
		"""
		Execute pending transaction
		:param transact: transact instance
		:return: transact
		"""
		status_id = 1

		if transact.status_id == status_id:
			return False

		status = TransactionStatus.objects.get(pk=status_id)

		transact.status = status
		transact.save()
		return transact

	def __to_archive(self, transact):
		"""
		Execute to archive transaction
		:param transact: transact instance
		:return: transact
		"""
		transact.is_archive = True
		transact.save()
		return transact

	def __from_archive(self, transact):
		"""
		Execute from archive transaction
		:param transact: transact instance
		:return: transact
		"""
		transact.is_archive = False
		transact.save()
		return transact

	def execute(self, transact):
		"""
		Execute action
		:param transact: transact instance
		:return: execution result
		"""
		result = self.__action(transact)
		if not result:
			self.__logger.error(Code.TRANSACT_EXE_ERR, action_id=self.__action_id, transact_id=transact.transact_id)
		return result