from django.conf.urls import url

from telephone.my_app.api import get_pbx_info, get_stat
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
]
