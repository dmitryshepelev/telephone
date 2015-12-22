from HTMLParser import HTMLParser


class HTMLTableParser(HTMLParser):
	def __init__(self, type=None, selector=None):
		HTMLParser.__init__(self)
		self.__selector_type = type
		self.__selector = selector
		self.__table = []
		self.__is_captured = False

	def handle_starttag(self, tag, attrs):
		if tag == 'table' and (self.__selector and self.__selector_type and attrs[self.__selector_type] == self.__selector):
			self.__is_captured = True

	def handle_endtag(self, tag):
		if tag == 'table':
			self.__is_captured = False

	def handle_data(self, data):
		if self.__is_captured and data and not data.isspace():
			self.__table.append(data)

	@property
	def table(self):
		"""
		Getter of __table
		:return: table value
		"""
		return self.__table