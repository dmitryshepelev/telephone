from django.conf.urls import include, url
from django.contrib import admin

from telephone import main_app, auth_app
from telephone.shared_views import default_error


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(main_app.urlpatterns)),
    url(r'^auth/', include(auth_app.urlpatterns)),
    url(r'e/$', default_error, {'template': 'default_error.html'})
]


handler404 = 'telephone.shared_views.default_404'