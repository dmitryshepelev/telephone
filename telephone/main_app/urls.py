from django.conf.urls import url

from telephone.main_app.views import main_resolver, get_statistic, get_call_record, pay, \
	get_call_cost, request_callback, get_call_cost_by_country, incoming_detect


urlpatterns = [
	url(r'^$', main_resolver, {'templates': ['panel.html', 'calls.html']}),
	url(r'^getCalls/$', get_statistic, {'template': 'calls-table.html'}),
	url(r'^getCallRecord/$', get_call_record),
	url(r'^getCallCost/$', get_call_cost),
	url(r'^getCallCostByCountry/$', get_call_cost_by_country),
	url(r'^requestCallback/$', request_callback),
	url(r'^pay/(?P<type>subfee|balance)/$', pay),
	url(r'^incd/$', incoming_detect)
]