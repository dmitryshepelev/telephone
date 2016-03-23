from django.conf.urls import url
from telephone.api.controllers import get_statistic

urlpatterns = [
	url(r'^getstat/$', get_statistic)
]
