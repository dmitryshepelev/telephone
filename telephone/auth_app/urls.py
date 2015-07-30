from django.conf.urls import url
from telephone.auth_app.views import login_page, sign_in, logout_user

urlpatterns = [
	url(r'^login/$', login_page, {'template': 'login.html'}),
	url(r'^signin/$', sign_in, {}),
	url(r'^logout/$', logout_user, {}),
]