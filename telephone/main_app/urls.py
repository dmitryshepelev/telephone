from django.conf.urls import url
from telephone.main_app.views import main, get_statistic, calls

urlpatterns = [
	url(r'^$', main, {'template': 'main.html'}),
	url(r'^calls/$', calls, {'template': 'calls.html'}),
	url(r'^getCalls/$', get_statistic, {'template': 'calls-table.html'}),
]