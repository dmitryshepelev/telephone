import datetime
from telephone import settings


class CallsFilterParams():
	def __init__(self, params=None):
		self.__params = {
			'date__gte': datetime.datetime.now().strftime(settings.DATETIME_FORMAT_START),
			'date__lte': datetime.datetime.now().strftime(settings.DATETIME_FORMAT_END),
		}
		# 0 - missed and answered; 1 - answered only; 2 - missed only
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
				self.__params['is_answered'] = False
			elif value == 2:
				self.__params['is_answered'] = True

	@property
	def params(self):
		"""
		Getter of __params
		:return: params
		"""
		return self.__params