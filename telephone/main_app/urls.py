from django.conf.urls import url
from telephone.main_app.views import main, get_test_file, calls

urlpatterns = [
	url(r'^$', main, {'template': 'main.html'}),
	url(r'^calls/$', calls, {'template': 'calls.html'}),
	url(r'^test/$', get_test_file),
]