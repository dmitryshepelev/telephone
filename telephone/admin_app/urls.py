from django.conf.urls import url

from telephone.admin_app.views import create_new_user, get_subscribe_transacts, get_pr_transacts


urlpatterns = [
	url(r'^newuser/$', create_new_user, {'template': 'create_new_user.html'}),
	url(r'^getTransacts/(?P<transact_type>pending|archive|history)/$', get_subscribe_transacts),
	url(r'^getPRTransacts/(?P<transact_type>pending|history)/$', get_pr_transacts),
]