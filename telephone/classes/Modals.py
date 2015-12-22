class Modal(object):
	"""
	Base Modal Instance class
	"""
	def __init__(self, name, params):
		self.__name = name
		self.__params = params or {}

	@property
	def template(self):
		"""
		Getter of __template
		:return: template value
		"""
		return '{name}_modal.html'.format(name=self.__name)

	@property
	def name(self):
		"""
		Getter of __name
		:return: name value
		"""
		return self.__name

	@name.setter
	def name(self, value):
		"""
		Setter of __name
		:param value: value to set
		"""
		self.__name = value

	@property
	def params(self):
		"""
		Getter of __params
		:return: params value
		"""
		return self.__params

	def __set_param(self, name, value):
		"""
		Set param by name
		:param name: name of the param
		:param value: param value to set
		"""
		self.__params.__setitem__(name, value)

	@staticmethod
	def factory(name, params):
		"""
		Factory method to create modal instance
		:param name: modal type name
		:param params: modal content params
		:return: concrete modal instance
		"""
		if name == 'callback':
			return CallbackModal(name, params)
		if name == 'callCostByCountry':
			return CallCostByCountryModal(name, params)
		else:
			return None


class CallbackModal(Modal):
	"""
	Concrete Modal Instance class
	"""
	def __init__(self, name, params):
		self.__params = {
			'number': params.get('number', '').encode()
		}
		super(CallbackModal, self).__init__(name, self.__params)

	@property
	def number(self):
		"""
		Getter of __number
		:return: number value
		"""
		return self.__params.get('number', '')

	@number.setter
	def number(self, value):
		"""
		Setter of __number
		:param value: value to set
		:return: number value
		"""
		name = 'number'
		self.__params.__setitem__(name, value)
		self.__set_param(name, value)


class CallCostByCountryModal(Modal):
	"""
	Concrete Modal instance class
	"""

	def __init__(self, name, params):
		super(CallCostByCountryModal, self).__init__(name, params)