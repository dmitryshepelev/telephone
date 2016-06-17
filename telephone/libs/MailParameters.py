# coding=utf-8
from telephone import settings


class MailParameters():
	def __init__(self, params):
		self.__params = {
			'domain': settings.DOMAIN,
			'login': params['login'],
			'password': params['password']
		}

	def get_params(self):
		return self.__params


class MailboxParameters():
	def __init__(self, login, **params):
		self.__params = {
			'domain': settings.DOMAIN,
			'login': login,
			'iname': 'Анатолий',
			'fname': 'Кузнецов',
			'hintq': '2+2',
			'hinta': '4'
		}
		if params:
			for key, value in params.items():
				self.__params[key] = params[key]

	def get_params(self):
		return self.__params
