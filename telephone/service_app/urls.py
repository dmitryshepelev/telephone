from django.conf.urls import url
from telephone.service_app.controllers import get_api_urls, get_oauth_token

urlpatterns = [
	url(r'^getApiUrls/', get_api_urls),
	url(r'^getOAuthToken/', get_oauth_token),
]
