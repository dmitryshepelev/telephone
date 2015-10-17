# coding=utf-8

import requests

from telephone import settings
from telephone.classes.ApiParams import ApiParams
from telephone.services import AppLogger


__logger = AppLogger('main_logger')


def get_logger():
	return __logger


def get_call_record(params, is_superuser):
	if settings.TEST_MODE or is_superuser:
		path = settings.BASE_DIR + '/static/content/test.mp3'
		return open(path, 'rb')

	request_string = '?%shash=%s' % (''.join('{}={}&'.format(key, value) for key, value in sorted(params.items())), ApiParams.Parameters.get_hash_string(params))
	url = '%s%s%s' % (settings.API_URLS['base_api_url'], settings.API_URLS['get_record'], request_string,)
	api_request = requests.get(url, headers={'Content-Disposition': 'attachment', 'filename': '%s.mp3' % (id,)})
	if api_request.ok:
		return api_request.content
	else:
		return None