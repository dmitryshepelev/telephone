from django.utils.module_loading import autodiscover_modules

from telephone.api.urls import urlpatterns


def autodiscover():
	autodiscover_modules('api', register_to=urlpatterns)