from base64 import b64encode
import hashlib
import datetime
import hmac

from telephone import settings


class Parameters():
	def __init__(self):
		pass

	__domain = settings.API_URLS['base_api_url']
	__api_version = settings.API_URLS['api_version']

	@staticmethod
	def generate_params_string(params):
		"""
		Generate request string from parameters
		:return: request string
		"""
		return '%s' % (''.join('{}={}&'.format(key, value) for key, value in sorted(params.items()))[:-1])

	@staticmethod
	def sha_encode(method_name, request_string, secret_key):
		"""
		Encode string with sha1 algorithm with secret ket
		:param method_name: api method name
		:param request_string: api request string
		:param secret_key: user secret key to api access
		:return: sha1 encoded string
		"""
		return hmac.new(secret_key, '%s%s?%s%s' % (Parameters.__api_version, method_name, request_string, hashlib.md5(request_string).hexdigest()), hashlib.sha1).hexdigest()

	@staticmethod
	def generate_sign(sha_string):
		"""
		Generate authorization sigh
		:param sha_string: sha1 encoded string
		:return: base64 encoded string
		"""
		return b64encode(sha_string)

	@staticmethod
	def get_domain_url(method):
		"""
		Generate high-level url to request
		:param method: api method name
		:return: domain url as 'https://domain/api_version/method'
		"""
		return '%s%s%s?' % (Parameters.__domain, Parameters.__api_version, method)


class CallsParameters(Parameters):
	__date_now = datetime.datetime.strptime(datetime.datetime.now().strftime(settings.DATETIME_FORMAT), settings.DATETIME_FORMAT)

	def __init__(self, start=__date_now, end=__date_now, sip='', cost_only='', type=''):
		Parameters.__init__(self)
		self.__params = {
			# Start date: 'd.m.Y' *Required*
			'start': start,
			# End date (inclusively): 'd.m.Y' *Required*
			'end': end,
			# Determine SIP number
			# 'sip': sip,
			# Wasted cash
			# 'cost_only': cost_only,
			# Call type: doesn't include - common; 'toll' - 800 number; ru495 - 495 number
			# 'type': type
		}
		self.__method = settings.API_URLS['statistics']

	def get_sign(self, secret_key):
		"""
		Generate authorization sign
		:param secret_key: user secret ket to api access
		:return: authorization sign
		"""
		request_string = Parameters.generate_params_string(self.__params)
		sha_string = Parameters.sha_encode(self.__method, request_string, secret_key)
		return Parameters.generate_sign(sha_string)

	def get_request_string(self):
		"""
		Generate full request string from parameters
		:return: request string
		"""
		return '%s%s' % (Parameters.get_domain_url(self.__method), Parameters.generate_params_string(self.__params))

	def set_params(self, params):
		"""
		Sets parameters
		:param params: array of parameters
		:return: None
		"""
		for key, value in params.items():
			self.__params[key] = params[key]


class MailParameters(Parameters):
	def __init__(self, params):
		Parameters.__init__(self)
		self.__params = {
			'domain': settings.DOMAIN,
			'login': params['login'],
			'password': params['email_password']
		}

	def get_request_string(self):
		return Parameters.generate_params_string(self.__params)

	def get_params(self):
		return self.__params