# coding=utf-8
import re


class LocalizeService():
	def __init__(self, value):
		self.__value = value
		self.__values = {
			'Thisfieldisrequired.': 'Не все поля заполнены',
			'Ensurethisvaluehasatleast': 'Значение слишком короткое',
			'Invalidusernameorpassword': 'Неверный логин или пароль'
		}

	@property
	def values(self):
		"""
		Getter of __values
		:return: values
		"""
		return self.__values

	def __localize(self):
		"""
		Localize value
		:return: localized value or None
		"""
		result = None
		value = self.__value.replace(' ', '')
		for k, v in self.values.iteritems():
			is_match = re.match(k, value)
			if is_match:

				result = v
				break
		return result

	def get_localized_value(self):
		"""
		Localize value
		:return: localized value or source value if value isn't found
		"""
		return self.__localize() or self.__value

	def get_value(self):
		"""
		Get value
		:return: localized value
		"""
		return self.values[self.__value] or 'Err: Locale not found'