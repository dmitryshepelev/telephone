from django.conf.urls import url
from telephone.service_app.controllers import get_api_urls, get_oauth_token, generate_password, create_mail

urlpatterns = [
	url(r'^getApiUrls/', get_api_urls),
	url(r'^getOAuthToken/', get_oauth_token),
	url(r'^generatePassword/$', generate_password),
	url(r'^createMail/$', create_mail),
]
