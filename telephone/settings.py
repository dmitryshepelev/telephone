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
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_u@*cvlhy#9(9))hbv6@w3+6hfx=btuegjm$@sxw7-ixdd^$%5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
	'*',
]

TEMPLATE_DEBUG = True

# Application definition

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	# 'telephone.main_app.templatetags',
	'telephone.main_app',
	'telephone.auth_app',
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
		'NAME': 'telephonedb',  # 'videomesrf',
		'USER': 'postgres',  # 'videomesrf'
		'PASSWORD': 'qwaszx@1',
		'HOST': 'localhost',  # 'localhost',
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
	'static/content/fonts',
	'static/content/themes/',
	'static/content/themes/default',
	# 'static/content/scripts/coffee',
	'static/content/scripts/javascript',
	'static/content/scripts/shared',
	'static/content',
	'static/content/images'
)

STATIC_URL = '/static/'

# STATIC_ROOT = 'static/root/'

TEMPLATE_DIRS = (
	os.path.join(BASE_DIR,  'templates'),
	os.path.join(BASE_DIR,  'main_app/templates'),
	os.path.join(BASE_DIR,  'auth_app/templates'),
)

LOGIN_URL = '/auth/login/'

TEST_MODE = False

SCHEMA_URL = '/calls/'

S_KEY = '0.l4lxhd71bhr'

API_URLS = {
	'base_api_url': 'http://sipuni.com/api/statistic',
	'get_record': '/record',
	'get_calls': '/export',
}

CORS_ORIGIN_ALLOW_ALL = (
	'sipuni.com'
)

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		'verbose': {
			'format': "\n[%(asctime)s] %(levelname)s [%(filename)s:%(lineno)s] %(message)s",
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
			'filename': 'debug.log',
			'formatter': 'verbose',
		},
		'app_logger_handler': {
			'level': 'INFO',
			'class': 'logging.handlers.RotatingFileHandler',
			'maxBytes': 10*1024*1024,
			'backupCount': 0,
			'filename': 'app_log.log',
			'formatter': 'verbose',
		},
		'auth_logger_handler': {
			'level': 'INFO',
			'class': 'logging.handlers.RotatingFileHandler',
			'maxBytes': 10*1024*1024,
			'backupCount': 0,
			'filename': 'auth.log',
			'formatter': 'verbose',
		},
		'main_logger_handler': {
			'level': 'INFO',
			'class': 'logging.handlers.RotatingFileHandler',
			'maxBytes': 10*1024*1024,
			'backupCount': 0,
			'filename': 'main.log',
			'formatter': 'verbose',
		},
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
		'auth_logger': {
			'handlers': ['auth_logger_handler'],
			'level': 'INFO',
			'propagate': True,
		},
		'main_logger': {
			'handlers': ['main_logger_handler'],
			'level': 'INFO',
			'propagate': True,
		},
	},
}