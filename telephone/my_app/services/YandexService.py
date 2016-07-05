from telephone.my_app.services.ServiceBase import ServiceBase, ServiceResultError


class YandexServiceResultError(ServiceResultError):
	"""
	Yandex Service result error
	"""
	pass


class YandexService(ServiceBase):
	"""
	Yandex Service
	"""
	def __init__(self, yandex_profile):
		self._profile = yandex_profile

	def _get_request_headers(self):
		"""
		Returns dict of request headers
		:return:
		"""
		return {
			'Content-Type': 'application/json',
			'Authorization': 'OAuth %s' % self._profile.token
		}
