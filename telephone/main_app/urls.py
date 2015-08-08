from django.conf.urls import url
from telephone.main_app.views import main, get_test_file, calls, get_test_record, get_period_modal_template, \
	schema_error

urlpatterns = [
	url(r'^$', main, {'template': 'main.html'}),
	url(r'^calls/$', calls, {'template': 'calls.html'}),
	url(r'^calls/get_period_modal_template/$', get_period_modal_template, {'template': 'period_modal_template.html'}),
	url(r'^test/$', get_test_file),
	url(r'^testrecord/$', get_test_record),
	url(r'^e/schema/$', schema_error, {'template': 'schema_error.html'}),
]