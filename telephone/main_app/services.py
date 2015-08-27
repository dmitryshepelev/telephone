# coding=utf-8
from random import randint
import datetime
import string
import random

import requests

from telephone import settings
from telephone.exceptions import ApiErrorException, MailErrorException
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


def get_statistics(params, user):
	"""
	Get statistics from api
	:param params: CallParameters instance
	:param user: User instance
	:return: json type
	"""
	if settings.TEST_MODE or user.is_superuser:
		abspath = open(settings.BASE_DIR + '/static/content/stat.csv', 'r')
		return parse_csv(abspath.read())

	request_string = params.get_request_string()
	api_response = requests.get(request_string, headers={'Authorization': '%s:%s' % ('b0e5ccb775f83d4d8a1f', params.get_sign(user.userprofile.secret_key))})
	if api_response.ok:
		return api_response.content
	else:
		raise ApiErrorException(api_response)


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


def get_random_number(length):
	return ''.join(['%s' % randint(0, 9) for num in range(0, length)])


def generate_email_password(email_id):
	return 'wt%s$%s' % (datetime.datetime.now().strftime('%d%m%y'), email_id)


def generate_random_password(length):
	return ''.join(random.SystemRandom().choice(settings.PASSWORD_SYMBOLS) for _ in range(length))


def create_domain_mail(params):
	request_string = 'https://pddimp.yandex.ru/api2/admin/email/add'
	params_string = params.get_request_string()
	api_response = requests.post(request_string, params_string, headers={'Method': 'POST', 'PddToken': settings.MAIL_A_TOKEN})
	if api_response.ok:
		pass
	else:
		raise MailErrorException(api_response)