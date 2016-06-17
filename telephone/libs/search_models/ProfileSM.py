class ProfileSM(object):
	def __init__(self, profile):
		self.__profile = profile

	@property
	def model(self):
		"""
		Getter of __model
		:return: model value
		"""
		return {
			'username': self.__profile.username,
			'email': self.__profile.email
		}