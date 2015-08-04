from django.conf.urls import url
from telephone.main_app.views import main, get_test_file, calls, get_test_record

urlpatterns = [
	url(r'^$', main, {'template': 'main.html'}),
	url(r'^calls/$', calls, {'template': 'calls.html'}),
	url(r'^test/$', get_test_file),
	url(r'^testrecord/$', get_test_record),
]