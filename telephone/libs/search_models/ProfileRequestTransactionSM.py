

class ProfileRequestTransactionSM(object):
	def __init__(self, transact):
		self.__transact = transact

	@property
	def model(self):
		"""
		Getter of __get_model
		:return: get_model value
		"""
		return {
			'transact_id': self.__transact.transact_id,
			'email': self.__transact.email,
		}