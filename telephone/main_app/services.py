# coding=utf-8

import requests

from telephone import settings
from telephone.main_app.proxy import Parameters
from telephone.main_app.proxy.Call import Call
from telephone.services import AppLogger


__logger = AppLogger('main_logger')


def get_logger():
	return __logger


def parse_csv(csv_string):
	arr = []
	delimiter = settings.DELIMITER
	csv_string = csv_string[:-1] if csv_string[-1] == '\n' else csv_string
	iter_csv = iter(csv_string.split('\n'))
	next(iter_csv)
	for item in iter_csv:
		arr.append(Call(item.split(delimiter)))
	return arr


def get_calls(params, is_superuser):
	if settings.TEST_MODE or is_superuser:
		abspath = open(settings.BASE_DIR + '/static/content/test.csv', 'r')
		return parse_csv(abspath.read())

	request_string = params.get_request_string()
	url = '%s%s%s' % (settings.API_URLS['base_api_url'], settings.API_URLS['get_calls'], request_string,)
	api_request = requests.get(url, headers={'Content-Disposition': 'attachment', 'filename': 'stat.csv'})
	if api_request.ok:
		return parse_csv(api_request.content)
	else:
		return None


def get_call_record(params, is_superuser):
	if settings.TEST_MODE or is_superuser:
		path = settings.BASE_DIR + '/static/content/test.mp3'
		return open(path, 'rb')

	request_string = '?%shash=%s' % (''.join('{}={}&'.format(key, value) for key, value in sorted(params.items())), Parameters.Parameters.get_hash_string(params))
	url = '%s%s%s' % (settings.API_URLS['base_api_url'], settings.API_URLS['get_record'], request_string,)
	api_request = requests.get(url, headers={'Content-Disposition': 'attachment', 'filename': '%s.mp3' % (id,)})
	if api_request.ok:
		return api_request.content
	else:
		return None