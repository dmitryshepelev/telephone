"""
Django settings for telephone project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import string
import time
import datetime
import uuid

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_u@*cvlhy#9(9))hbv6@w3+6hfx=btuegjm$@sxw7-ixdd^$%5'

MAIL_A_TOKEN = 'FY6DV6SXQ2MNIW44F3ZPUQ3HDUP5P22N54I7ZBTUAXMD42PS6KZA'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
	'*',
]

TEMPLATE_DEBUG = False

TEST_MODE = False

DOMAIN = 'web-tel.ru'

INFO_EMAIL = 'info@web-tel.ru'

# Application definition

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	# 'telephone.main_app.templatetags',
	# 'telephone.main_app',
	'telephone.auth_app',
	# 'telephone.service_app',
	# 'telephone.admin_app',
	# 'celery',
	'telephone.my_app'
)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'telephone.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(BASE_DIR, 'templates')],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

WSGI_APPLICATION = 'telephone.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'webtel_db' if DEBUG else 'videomesrf',
		'USER': 'postgres' if DEBUG else 'videomesrf',
		'PASSWORD': 'qwaszx@1',
		'HOST': 'localhost' if DEBUG else 'pg.sweb.ru',
		'PORT': '5432',
	}
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATICFILES_DIRS = (
	'telephone/auth_app/scripts/',
	'telephone/my_app/scripts/',

	'static/content/fonts',
	'static/content/themes/',
	# 'static/content/scripts/coffee',
	'static/content/scripts/javascript',
	'static/content/scripts/shared',
	'static/content/scripts/common',
	'static/content',
	'static/content/images',
	'static',
	'static/content/res',
)

STATIC_URL = '/static/content/'

STATIC_ROOT = 'static/r_content/'

TEMPLATE_DIRS = (
	os.path.join(BASE_DIR,  'templates'),
	os.path.join(BASE_DIR,  'main_app/templates'),
	os.path.join(BASE_DIR,  'auth_app/templates'),
	os.path.join(BASE_DIR,  'admin_app/templates'),
	os.path.join(BASE_DIR,  'servise_app/templates'),
	os.path.join(BASE_DIR,  'static/email_templates'),
)

LOGIN_URL = '/auth/'

S_KEY = 'e6eddf38406a4fa03d09'

PBX = {
	'host': 'https://api.zadarma.com/',
	'version': 'v1',
	'urls': {
		'balance': '/info/balance/',
		'common_stat': '/statistics/',
		'pbx_stat': '/statistics/pbx/',
		'call_cost': '/info/price/'
	}
}

YANDEX = {
	'disk': {
		'default_dir_name': 'pbxrec',
		'host': 'https://cloud-api.yandex.net/v1/disk/resources',
		'create_dir': '?path=',
		'upload_link': '/upload?path=',
		'download_link': '/download?path=',
	}
}

API_URLS = {
	'api': {
		'host': 'https://api.zadarma.com',
		'api_version': '/v1',
		'common_stat': '/statistics',
		'pbx_stat': '/statistics/pbx',
		'balance': '/v1/info/balance',
		'call_cost': '/info/price/',
		'request_callback': '/request/callback/',
		'sip': '/sip/',
		'get_redirects': '/sip/redirection/',
		'internal_numbers': '/pbx/internal/'
	},
	'base_api_url': 'https://api.zadarma.com',
	'api_version': '/v1',
	'get_record': '/record',
	'statistics': '/statistics',
	'statisticspbx': '/statistics/pbx',
	'oauth': {
		'host': 'https://oauth.yandex.ru',
		'authorize': '/authorize?response_type=code',
		'token': '/token'
	},
	'mail': {
		'host': 'https://pddimp.yandex.ru',
		'create_mail': '/api2/admin/email/add',
		'update_mail': '/api2/admin/email/edit',
		'download_attach': 'https://mail.yandex.by/message_part/{filename}?_uid={uid}&name={filename}'
	},
	'disk': {
		'host': 'https://cloud-api.yandex.net/v1/disk/resources',
		'file_download_link': '/download?path=',
		'file_upload_link': '/upload?path=',
		'files_info': '/files',
		'create_folder': '?path='
	}
}

TEMP_DIR = 'static/temp/'

TIME_CORRECTION_SEC = 3
TIME_CORRECTION_MIN = 1

O_AUTH_ID = '52a0d804d54b45ef8c309088af6d444d'

O_AUTH_SECRET = '962a08aad3974d3395c140a77b0f26ac'

CORS_ORIGIN_ALLOW_ALL = (
	'*'
)

DELIMITER = ';'

DATE_CLIENT_FORMAT = '%d.%m.%Y'
DATETIME_FORMAT = '%d.%m.%Y %H:%M:%S'
DATETIME_FORMAT_ALTER = '%Y-%m-%d %H:%M:%S'
DATETIME_FORMAT_START = '%Y-%m-%d 00:00:00'
DATETIME_FORMAT_END = '%Y-%m-%d 23:59:59'

WS_SCRIPT_TEMPLATE_NAME = 'ws_code.html'

PAYMENT_DATA = {
	'scid': '5703',
	'shop_id': '13582',
	'sum': '50',
	'customer_number': ''
}

W_NUMBER = '41001864034525'
DEFAULT_SUBSCRIPTION_PAYMENT = 500
DEFAULT_SUBCRIPTION_PAYMENT_TYPE = 'PC'
SUBSCRIPTION_DATA = {
	'receiver': W_NUMBER,
	'form_comment': 'form comment',
	'short_dest': 'short_dest',
	'quickpay_form': 'shop',
	'targets': 'targets',
	'sum': DEFAULT_SUBSCRIPTION_PAYMENT,
	'payment_type': DEFAULT_SUBCRIPTION_PAYMENT_TYPE,
	'label': ''
}

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		'verbose': {
			'format': "\n[%(asctime)s] %(levelname)s %(message)s",
			'datefmt': "%d/%b/%Y %H:%M:%S"
		},
		'simple': {
			'format': '%(levelname)s %(message)s'
		},
	},
	'handlers': {
		'django': {
			'level': 'INFO',
			'class': 'logging.handlers.RotatingFileHandler',
			'maxBytes': 10*1024*1024,
			'backupCount': 0,
			'filename': os.path.join(BASE_DIR,  'debug.log'),
			'formatter': 'verbose',
		},
		'app_logger_handler': {
			'level': 'INFO',
			'class': 'logging.handlers.RotatingFileHandler',
			'maxBytes': 10*1024*1024,
			'backupCount': 0,
			'filename': os.path.join(BASE_DIR,  'log.log'),
			'formatter': 'verbose',
		}
	},
	'loggers': {
		'django': {
			'handlers': ['django'],
			'level': 'INFO',
			'propagate': True,
		},
		'app_logger': {
			'handlers': ['app_logger_handler'],
			'level': 'INFO',
			'propagate': True,
		},
	},
}