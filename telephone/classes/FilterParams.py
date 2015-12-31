import datetime
from django.db.models import Q
import operator
from telephone import settings
from telephone.service_app.services.CommonService import CallsConstants


class CallsFilterParams():
	def __init__(self, params=None):
		self.__params = {
			'date__gte': datetime.datetime.now().strftime(settings.DATETIME_FORMAT_START),
			'date__lte': datetime.datetime.now().strftime(settings.DATETIME_FORMAT_END),
		}
		# 0 - missed and answered; 1 - answered only; 2 - missed only
		self.__exclude_params = {}
		self.__call_type_query = Q(Q(call_type=CallsConstants.COMING) | Q(call_type=CallsConstants.INTERNAL) | Q(call_type=CallsConstants.INCOMING))
		self.set_params(params)

	def set_params(self, params):
		"""
		Sets parameters
		:param params: array of parameters
		:return: None
		"""
		if 'start' in params:
			self.__params['date__gte'] = datetime.datetime.strptime(params['start'], settings.DATE_CLIENT_FORMAT).strftime(settings.DATETIME_FORMAT_START)
		if 'end' in params:
			self.__params['date__lte'] = datetime.datetime.strptime(params['end'], settings.DATE_CLIENT_FORMAT).strftime(settings.DATETIME_FORMAT_END)
		if 'status' in params:
			value = int(params['status'])
			if value == 1:
				self.__exclude_params['disposition'] = CallsConstants.ANSWERED
			elif value == 2:
				self.__params['disposition'] = CallsConstants.ANSWERED
		if 'call_type' in params:
			value = params['call_type']
			types = value.split('|')
			self.__call_type_query = reduce(operator.or_, (Q(call_type=t) for t in types if t is not ''))

	@property
	def params(self):
		"""
		Getter of __params
		:return: params
		"""
		return self.__params

	@property
	def exclude_params(self):
		"""
		Getter of __exclude_params
		:return: exclude_params value
		"""
		return self.__exclude_params

	@property
	def call_type_query(self):
		"""
		Getter of __call_type_query
		:return: call_type_query value
		"""
		return self.__call_type_query