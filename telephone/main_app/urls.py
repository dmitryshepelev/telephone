from django.conf.urls import url

from telephone.main_app.views import main_resolver, get_statistic, get_call_record, get_profile_info, pay, \
	get_call_cost, request_callback, get_call_cost_by_country


urlpatterns = [
	url(r'^$', main_resolver, {'templates': ['panel.html', 'calls.html']}),
	url(r'^getCalls/$', get_statistic, {'template': 'calls-table.html'}),
	url(r'^getCallRecord/$', get_call_record),
	url(r'^getProfileInfo/$', get_profile_info, {'template': 'profile_info.html'}),
	url(r'^getCallCost/$', get_call_cost),
	url(r'^getCallCostByCountry/$', get_call_cost_by_country),
	url(r'^requestCallback/$', request_callback),
	url(r'^pay/(?P<type>subfee|balance)/$', pay),
]