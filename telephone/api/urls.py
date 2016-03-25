from django.conf.urls import url
from telephone.api.controllers import get_statistic, get_call_cost, cb_call

urlpatterns = [
	url(r'^getstat/$', get_statistic),
	url(r'^getcallcost/$', get_call_cost),
	url(r'^cbcall/$', cb_call)
]
