from django.conf.urls import url

from telephone.main_app.pages import st_page, ui_view, base, check_cost_page, callback_page, subfee_page, balance_page, \
	get_widget_script_page
from telephone.main_app.views import get_statistic, get_call_record, pay, \
	get_call_cost, request_callback, get_call_cost_by_country, incoming_detect, check_incoming_info, get_widget_script, \
	main_resolver


urlpatterns = [
	url(r'^$', main_resolver, {'templates': ['panel.html', 'my_base.html']}),

	url(r'^getCalls/$', get_statistic, {'template': 'calls-table.html'}),
	url(r'^getCallRecord/$', get_call_record),
	url(r'^getCallCost/$', get_call_cost),
	url(r'^getCallCostByCountry/$', get_call_cost_by_country),
	url(r'^requestCallback/$', request_callback),
	url(r'^pay/(?P<type>subfee|balance)/$', pay),
	url(r'^incd/(?P<user_key>[a-zA-Z0-9]{20})/$', incoming_detect),
	url(r'^chkinc/(?P<guid>[a-zA-Z0-9]{40})/$', check_incoming_info),
	url(r'^getscript/$', get_widget_script),

	# url(r'^$', base),
	url(r'^uiview/$', ui_view),
	url(r'^st/$', st_page),
	url(r'^cst/$', check_cost_page),
	url(r'^clb/$', callback_page),
	url(r'^sf/$', subfee_page),
	url(r'^blc/$', balance_page),
	url(r'^gscpt/$', get_widget_script_page)
]