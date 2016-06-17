from django.conf.urls import include, url
from django.contrib import admin

from telephone import auth_app, service_app, admin_app, api, my_app


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', include(admin_app.urlpatterns)),
    url(r'^', include(my_app.urlpatterns)),
    url(r'^auth/', include(auth_app.urlpatterns)),
    url(r'^services/', include(service_app.urlpatterns)),
    # url(r'^api/', include(api.urlpatterns)),
]


handler404 = 'telephone.shared_views.default_404'