from django.conf.urls import url
from telephone.admin_app.views import create_new_user

urlpatterns = [
	url(r'^newUser/$', create_new_user, {'template': 'create_new_user.html'}),
]
