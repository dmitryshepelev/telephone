from django.conf.urls import url

from telephone.auth_app.api import login, profile_request
from telephone.auth_app.views import login_page, logout_user, base, ui_view

urlpatterns = [
	url(r'^$', base),
	url(r'^uiview/$', ui_view),
	url(r'^login/$', login_page),
	url(r'^logout/$', logout_user, {}),

	url(r'api/login/$', login),
	url(r'api/profile_request/$', profile_request),
]
