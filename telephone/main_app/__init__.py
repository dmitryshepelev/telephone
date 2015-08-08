from django.utils.module_loading import autodiscover_modules

from telephone.main_app.models import Schema
from telephone.main_app.urls import urlpatterns


def autodiscover():
    autodiscover_modules('main_app', register_to=urlpatterns)