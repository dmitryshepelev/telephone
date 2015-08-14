# coding=utf-8
import hashlib
import time

import requests

from telephone import settings
from telephone.services import AppLogger
from telephone.settings import BASE_DIR


__logger = AppLogger('main_logger')


class Call():
	def __init__(self, arr):
		self.__incoming = True if 'входящий' == arr[0] else False if 'исходящий' == arr[0] else None
		self.__status = True if 'отвечен' == arr[1] else False
		self.__time = time.strptime(arr[2], '%d.%m.%Y %H:%M:%S')
		self.__from = arr[4]
		self.__responder = arr[6]
		self.__callTime = int(arr[7]) if arr[7] else 0
		self.__talkTime = int(arr[8]) if arr[8] else 0
		self.__recordId = arr[11]


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


def parse_csv(csv_string):
	arr = []
	delimiter = settings.DELIMITER
	csv_string = csv_string[:-1] if csv_string[-1] == '\n' else csv_string
	iter_csv = iter(csv_string.split('\n'))
	next(iter_csv)
	for item in iter_csv:
		arr.append(Call(item.split(delimiter)))
	return arr


def get_calls(request):
	if settings.TEST_MODE or request.user.is_superuser:
		abspath = open(BASE_DIR + '/static/content/test.csv', 'r')
		return parse_csv(abspath.read())

	request_string = get_request_string(request.GET)
	url = '%s%s%s' % (settings.API_URLS['base_api_url'], settings.API_URLS['get_calls'], request_string,)
	api_request = requests.get(url, headers={'Content-Disposition': 'attachment', 'filename': 'stat_%s-%s' % (request.GET.get('form'), request.GET.get('to'))})
	if api_request.ok:
		return parse_csv(api_request.content)
	else:
		return None