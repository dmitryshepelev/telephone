# coding=utf-8
class AuthorizeError(Exception):
	def __init__(self, **kwargs):
		self.message = 'Неверный логин или пароль'
