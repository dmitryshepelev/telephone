import uuid
from telephone import settings


class SubscriptionData():
	def __init__(self):
		self.__receiver = settings.W_NUMBER
		self.__form_comment = 'from comments'
		self.__short_dest = 'form comments'
		self.__quickpay_form = 'shop'
		self.__targets = 'targets'
		self.__sum = 500
		self.__payment_type = 'PC'
		self.__label = str(uuid.uuid4())

	@property
	def receiver(self):
		"""
		Getter of __receiver
		:return: receiver value
		"""
		return self.__receiver

	@receiver.setter
	def receiver(self, value):
		"""
		Setter of __receiver
		:param value: value to set
		"""
		self.__receiver = value

	@property
	def form_comment(self):
		"""
		Getter of __form_comments
		:return: form_comments value
		"""
		return self.__form_comment

	@form_comment.setter
	def form_comment(self, value):
		"""
		Setter of __form_comments
		:param value: value to set
		"""
		self.__form_comment = value

	@property
	def short_dest(self):
		"""
		Getter of __short_dest
		:return: short_dest value
		"""
		return self.__short_dest

	@short_dest.setter
	def short_dest(self, value):
		"""
		Setter of __short_dest
		:param value: value to set
		"""
		self.__short_dest = value

	@property
	def quickpay_form(self):
		"""
		Getter of __quickpay_form
		:return: quickpay_form value
		"""
		return self.__quickpay_form

	@quickpay_form.setter
	def quickpay_form(self, value):
		"""
		Setter of __quickpay_form
		:param value: value to set
		"""
		self.__quickpay_form = value

	@property
	def targets(self):
		"""
		Getter of __targets
		:return: targets value
		"""
		return self.__targets

	@targets.setter
	def targets(self, value):
		"""
		Setter of __targets
		:param value: value to set
		"""
		self.__targets = value

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
	def payment_type(self):
		"""
		Getter of __payment_type
		:return: payment_type value
		"""
		return self.__payment_type

	@payment_type.setter
	def payment_type(self, value):
		"""
		Setter of __payment_type
		:param value: value to set
		"""
		self.__payment_type = value

	@property
	def label(self):
		"""
		Getter of __label
		:return: label value
		"""
		return self.__label