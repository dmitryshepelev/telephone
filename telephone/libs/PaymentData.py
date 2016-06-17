class PaymentData():
	def __init__(self, customer_number=None):
		self.__scid = 5703
		self.__shop_id = 13582
		self.__sum = 50
		self.__customer_number = customer_number

	@property
	def scid(self):
		"""
		Getter of __scid
		:return: scid value
		"""
		return self.__scid

	@property
	def shop_id(self):
		"""
		Getter of __shop_id
		:return: shop_id value
		"""
		return self.__shop_id

	@property
	def sum(self):
		"""
		Getter of __sum
		:return: sum value
		"""
		return self.__sum

	@sum.setter
	def sum(self, value):
		"""
		Setter of __sum
		:param value: value to set
		"""
		self.__sum = value

	@property
	def customer_number(self):
		"""
		Getter of __customer_number
		:return: customer_number value
		"""
		return self.__customer_number

	@customer_number.setter
	def customer_number(self, value):
		"""
		Setter of __customer_number
		:param value: value to set
		"""
		self.__customer_number = value