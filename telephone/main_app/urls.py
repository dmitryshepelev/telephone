from django.conf.urls import url
from telephone.main_app.views import main_resolver, get_statistic, calls, get_call_record, get_profile_info, pay

urlpatterns = [
	url(r'^$', main_resolver, {'templates': ['panel.html', 'calls.html']}),
	url(r'^getCalls/$', get_statistic, {'template': 'calls-table.html'}),
	url(r'^getCallRecord/$', get_call_record),
	url(r'^getProfileInfo/$', get_profile_info, {'template': 'profile_info.html'}),
	url(r'^pay/$', pay, {'template': 'pay.html'}),
]