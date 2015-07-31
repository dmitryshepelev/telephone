from django.conf.urls import url
from telephone.main_app.views import main, about, get_test_file

urlpatterns = [
	url(r'^$', main, {'template': 'main.html'}),
	url(r'^about/$', about, {'template': 'about.html'}),
    url(r'^test/$', get_test_file),
]