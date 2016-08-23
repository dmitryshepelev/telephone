from django.conf.urls import url

from telephone.my_app.api import get_pbx_info, get_stat, get_call_cost, get_call_record_file, get_costs_by_country, \
	get_ws_script
from telephone.my_app.views import *

urlpatterns = [
	url(r'^$', main_resolver),
	url(r'^uiview/$', ui_view),
	url(r'^st/$', st_page),
	url(r'^cst/$', check_cost_page),
	url(r'^clb/$', callback_page),
	url(r'^sf/$', subfee_page),
	url(r'^blc/$', balance_page),
	url(r'^gscpt/$', get_widget_script_page),

	url(r'api/getpbxinfo/$', get_pbx_info),
	url(r'api/getstat/$', get_stat),
	url(r'api/getcallcost/$', get_call_cost),
	url(r'api/getcrfile/$', get_call_record_file),
	url(r'api/getcostbycountry/$', get_costs_by_country),
	url(r'api/getwsscript/$', get_ws_script)
]
