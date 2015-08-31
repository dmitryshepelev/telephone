# coding=utf-8
import json
from random import randint
import datetime
import random

import requests
from django.contrib.auth.models import User

from telephone import settings
from telephone.exceptions import ApiErrorException, MailErrorException
from telephone.main_app.models import UserProfile
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
	"""
	Generate random number
	:param length: number of numbers
	:return: string number
	"""
	return ''.join(['%s' % randint(0, 9) for _ in range(0, length)])


def generate_email_password(email_id):
	"""
	Generate password based on template: 'wt[day][month][year]$[login]
	:param email_id: user's login
	:return: string password
	"""
	return 'wt%s$%s' % (datetime.datetime.now().strftime('%d%m%y'), email_id)


def generate_random_password(length):
	"""
	Generate random password form letters and numbers
	:param length: length of password
	:return: string password
	"""
	return ''.join(random.SystemRandom().choice(settings.PASSWORD_SYMBOLS) for _ in range(length))


def create_domain_mail(params):
	"""
	Create new domain email.
	:param params: MailParameters instance
	:return: api response data: {'domain': 'name', 'login': 'email', 'uid': 'uid, 'success': 'status'}
	"""
	request_string = '%s%s' % (settings.API_URLS['mail']['host'], settings.API_URLS['mail']['create_mail'])
	api_response = requests.post(request_string, params.get_params(), headers={'PddToken': settings.MAIL_A_TOKEN})
	if api_response.ok:
		response_data = json.loads(api_response.content)
		if response_data['success'] == 'ok':
			return response_data
		else:
			raise MailErrorException(response_content=response_data)
	else:
		raise ApiErrorException(api_response=api_response)


def get_oauth_token(code):
	"""
	Get OAuth token to api access
	:param code: verifying code
	:return: api response data: {'access_token': 'token', 'token_type': 'bearer', 'expires_in': 'time_in_seconds'}
	"""
	request_string = '%s%s' % (settings.API_URLS['oauth']['host'], settings.API_URLS['oauth']['token'])
	api_response = requests.post(request_string, {'grant_type': 'authorization_code', 'code': code, 'client_id': settings.O_AUTH_ID, 'client_secret': settings.O_AUTH_SECRET}, headers={'Content-type': 'application/x-www-form-urlencoded'})
	if api_response.ok:
		response_data = json.loads(api_response.content)
		return response_data
	else:
		raise ApiErrorException(api_response=api_response)


def create_profile(data):
	"""
	Creates a new user and userProfile
	:param data: NewUserForm data instance
	:return: User instance
	"""
	user = User.objects.create_user(username=data['userName'], email=data['userEmail'], password=data['userPassword'])
	user.save()
	user_profile = UserProfile.objects.create(profile_email='%s@%s' % (data['login'], settings.DOMAIN), profile_password=data['password'], uid=data['uid'], token=data['token'], user_key=data['userKey'], secret_key=data['secretKey'], user_id=user.id)
	user_profile.save()
	return user