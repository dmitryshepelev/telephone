from django.conf.urls import url
from telephone.main_app.views import main, get_statistic, calls, get_call_record, get_period_modal_template, \
	schema_error

urlpatterns = [
	url(r'^$', main, {'template': 'main.html'}),
	url(r'^calls/$', calls, {'template': 'calls.html'}),
	url(r'^calls/get_period_modal_template/$', get_period_modal_template, {'template': 'period_modal_template.html'}),
	url(r'^getCalls/$', get_statistic, {'template': 'calls-table.html'}),
	url(r'^getCallRecord/$', get_call_record),
	url(r'^e/schema/$', schema_error, {'template': 'schema_error.html'}),
]