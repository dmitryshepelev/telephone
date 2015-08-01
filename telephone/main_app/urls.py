from django.conf.urls import url
from telephone.main_app.views import main, stat, get_test_file

urlpatterns = [
	url(r'^$', main, {'template': 'main.html'}),
	url(r'^stat/$', stat, {'template': 'stat.html'}),
	url(r'^test/$', get_test_file),
]