from django.utils.module_loading import autodiscover_modules
from telephone.auth_app.urls import urlpatterns


def autodiscover():
    autodiscover_modules('auth_app', register_to=urlpatterns)