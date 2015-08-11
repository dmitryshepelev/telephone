import hashlib
import logging
from telephone import settings
from telephone.services import AppLogger

__logger = AppLogger('main_logger')


def get_logger():
	return __logger


def get_hash_string(params):
	"""
	Calculates md5 hash string
	:param params: source params dict
	:return: md5 hash string
	"""
	return hashlib.md5('%s%s' % (''.join('{}+'.format(value) for key, value in sorted(params.items())), settings.S_KEY,)).hexdigest()


def get_request_string(params):
	"""
	Generate request string from parameters
	:param params: dictionary of parameters
	:return: request string
	"""
	return '?%shash=%s' % (''.join('{}={}&'.format(key, value) for key, value in sorted(params.items())), get_hash_string(params))