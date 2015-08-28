from django.conf.urls import url
from telephone.main_app.views import main, get_statistic, calls, get_call_record, schema_error, create_new_user, \
	generate_password, create_mail, get_api_urls, get_api_token

urlpatterns = [
	url(r'^$', main, {'template': 'main.html'}),
	url(r'^calls/$', calls, {'template': 'calls.html'}),
	url(r'^getCalls/$', get_statistic, {'template': 'calls-table.html'}),
	url(r'^getCallRecord/$', get_call_record),
	url(r'^e/schema/$', schema_error, {'template': 'schema_error.html'}),
	url(r'^admin/newUser/$', create_new_user, {'template': 'create_new_user.html'}),
	url(r'^generatePassword/$', generate_password),
	url(r'^createMail/$', create_mail),
	url(r'^getApiUrls/$', get_api_urls),
	url(r'^getApiToken/$', get_api_token),
]