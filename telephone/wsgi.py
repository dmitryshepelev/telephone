import os, sys
from telephone import settings

if not settings.DEBUG:
	sys.path.insert(0, '/home/v/videomesrf/tel/public_html')
	sys.path.insert(0, '/home/v/videomesrf/tel')
	sys.path.insert(0, '/home/v/videomesrf/tel/.djangovenv/lib64/python2.7/site-packages')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "telephone.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()