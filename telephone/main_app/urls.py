from django.conf.urls import url
from telephone.main_app.views import main

urlpatterns = [
	url(r'^$', main, {'template': 'main.html'}),
]