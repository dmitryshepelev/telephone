class MessageTypes:
	def __init__(self):
		pass

	SUCCESS = 'success'
	ERROR = 'error'
	WARNING = 'warning'
	INFO = 'info'


class Message(object):

	@classmethod
	def __get_obj(cls, obj_type, text=None, header=None):
		"""
		Returns dict of Message
		:param obj_type: 'success', 'error', 'warning' or 'info'
		:param text: text
		:param header: header
		:return: dict
		"""
		obj = dict(type=obj_type)

		if text:
			obj.__setitem__('text', text)

		if header:
			obj.__setitem__('header', header)

		return obj

	@classmethod
	def success(cls, text=None, header=None):
		"""
		Returns success message
		:param text:
		:param header:
		:return:
		"""
		return cls.__get_obj(MessageTypes.SUCCESS, text, header)

	@classmethod
	def error(cls, text=None, header=None):
		"""
		Returns error message
		:param text:
		:param header:
		:return:
		"""
		return cls.__get_obj(MessageTypes.ERROR, text, header)

	@classmethod
	def warning(cls, text=None, header=None):
		"""
		Returns warning message
		:param text:
		:param header:
		:return:
		"""
		return cls.__get_obj(MessageTypes.WARNING, text, header)

	@classmethod
	def info(cls, text=None, header=None):
		"""
		Returns info message
		:param text:
		:param header:
		:return:
		"""
		return cls.__get_obj(MessageTypes.INFO, text, header)
