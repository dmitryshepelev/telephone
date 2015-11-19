from django.conf.urls import url
from telephone.auth_app.views import login, logout_user, new_profile_request

urlpatterns = [
	url(r'^login/$', login, {'template': 'login.html'}),
	url(r'^newProfileRequest/$', new_profile_request, {'template': 'new_profile_request_succeed.html'}),
	url(r'^logout/$', logout_user, {}),
]