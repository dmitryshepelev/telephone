# coding=utf-8
import time
import datetime
from telephone.service_app.services.CommonService import CallsConstants


class Call():
	def __init__(self, data):
		self.call_id = data['id']
		self.sip = data['sip']
		self.date = datetime.datetime.strptime(data['callstart'], '%Y-%m-%d %H:%M:%S')
		self.caller = data['from']
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
		self.disposition = None

		# stat
		self.description = None
		self.bill_seconds = None
		self.cost = None
		self.bill_cost = None
		self.currency = None

		self.call_type = None

		self.__is_first_call = False

		if call:
			self.__init_with_instance(call)

	def __init_with_instance(self, call):
		"""
		Init class with database instance
		:param call: Call model
		"""
		self.set_params(**call.__dict__)
		self.sip = call.callee.sip
		self.description = call.callee.description
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


class CallsStat():
	def __init__(self, calls=None):
		self.__total = 0
		self.__new = 0
		self.__coming = 0
		self.__incoming = 0
		self.__missed = 0
		self.__internal = 0

		if calls:
			self.calculate_stat(calls)

	@property
	def total(self):
		"""
		Property getter
		:return: property value
		"""
		return self.__total

	@property
	def new(self):
		"""
		Property getter
		:return: property value
		"""
		return self.__new

	@property
	def coming(self):
		"""
		Property getter
		:return: property value
		"""
		return self.__coming

	@property
	def incoming(self):
		"""
		Property getter
		:return: property value
		"""
		return self.__incoming

	@property
	def missed(self):
		"""
		Property getter
		:return: property value
		"""
		return self.__missed

	@property
	def internal(self):
		"""
		Getter of __internal
		:return: internal value
		"""
		return self.__internal

	def calculate_stat(self, calls):
		"""
		Calculate calls stat
		:param calls:
		:return:
		"""
		self.__init__()
		for call in calls:
			self.__total += 1
			if call.is_first_call:
				self.__new += 1
			if not call.disposition == 'answered':
				self.__missed += 1
			if call.call_type == CallsConstants.INTERNAL:
				self.__internal += 1
			if call.call_type == CallsConstants.INCOMING:
				self.__incoming += 1
			if call.call_type == CallsConstants.COMING:
				self.__coming += 1