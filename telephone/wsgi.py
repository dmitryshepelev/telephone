import os
import sys

DEBUG = True
if not DEBUG:
	sys.path.insert(0, '/home/v/videomesrf/my.web-tel.ru/public_html')
	sys.path.insert(0, '/home/v/videomesrf/my.web-tel.ru')
	sys.path.insert(0, '/home/v/videomesrf/my.web-tel.ru/.djangovenv/lib64/python2.7/site-packages')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "telephone.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()