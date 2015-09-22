from django.conf.urls import url
from telephone.auth_app.views import login, logout_user

urlpatterns = [
	url(r'^login/$', login, {'template': 'login.html'}),
	url(r'^logout/$', logout_user, {}),
]