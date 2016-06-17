from django.utils.module_loading import autodiscover_modules

from telephone.my_app.urls import urlpatterns


def autodiscover():
	autodiscover_modules('my_app', register_to=urlpatterns)