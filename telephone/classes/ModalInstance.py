class ModalInstance(object):
	def __init__(self, modal_name, modal_params):
		self.__template = '{name}_modal.html'.format(name=modal_name)
		self.__params = modal_params or {}

	@property
	def template(self):
		"""
		Getter of __template
		:return: template value
		"""
		return self.__template

	@property
	def params(self):
		"""
		Getter of __params
		:return: params value
		"""
		return self.__params