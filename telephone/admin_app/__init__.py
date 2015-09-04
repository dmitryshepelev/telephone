from django.utils.module_loading import autodiscover_modules
from telephone.admin_app.urls import urlpatterns


def autodiscover():
    autodiscover_modules('admin_app', register_to=urlpatterns)