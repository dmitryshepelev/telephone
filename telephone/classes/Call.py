# coding=utf-8
import time
import datetime


class Call():
	def __init__(self, data):
		self.call_id = data['id']
		self.sip = data['sip']
		self.date = datetime.datetime.strptime(data['callstart'], '%Y-%m-%d %H:%M:%S')
		self.destination = data['to']
		self.description = data['description']
		self.disposition = data['disposition']
		self.bill_seconds = data['billseconds']
		self.cost = data['cost']
		self.bill_cost = data['billcost']
		self.currency = data['currency']


class CallPBX():
	def __init__(self, data):
		self.call_id = data['call_id']
		self.sip = data['sip']
		self.date = datetime.datetime.strptime(data['callstart'], '%Y-%m-%d %H:%M:%S')
		self.destination = data['destination']
		self.disposition = data['disposition']
		self.seconds = data['seconds']
		self.clid = data['clid']


class CallRecord():
	def __init__(self, call=None):
		self.call_id = None
		self.clid = None
		self.sip = None
		self.date = None
		self.destination = None
		self.description = None
		self.disposition = None
		self.bill_seconds = None
		self.cost = None
		self.bill_cost = None
		self.currency = None

		self.__is_answered = True
		self.__is_first_call = False

		if call:
			self.__init_with_instance(call)

	def __init_with_instance(self, call):
		self.set_params(**call.__dict__)
		self.sip = call.callee.sip
		self.description = call.callee.description
		self.__is_answered = call.is_answered
		self.__is_first_call = call.callee.first_call_date == call.date

	def set_params(self, **kwargs):
		"""
		Sets the params by name
		:param kwargs: params
		:return: None
		"""
		if not kwargs:
			return None

		for key, value in kwargs.items():
			if key in vars(self):
				setattr(self, key, value)

	@property
	def is_answered(self):
		"""
		Getter of __is_answered
		:return: is_answered
		"""
		return self.__is_answered

	@is_answered.setter
	def is_answered(self, value):
		"""
		Setter of __is_answered
		:param value: value to set
		:return: TypeError if value isn't type of bool
		"""
		if type(value) is bool:
			self.__is_answered = value
		else:
			raise TypeError

	@property
	def is_first_call(self):
		"""
		Getter of __is_first_call
		:return: is_first_call
		"""
		return self.__is_first_call

	@is_first_call.setter
	def is_first_call(self, value):
		"""
		Setter of __is_first_call
		:param value: value to set
		:return: TypeError if value isn't type of bool
		"""
		if type(value) is bool:
			self.__is_first_call = value
		else:
			raise TypeError