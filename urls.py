# pylint: disable=line-too-long, wrong-import-position

from django.urls import path

from .views import ip_info

urlpatterns = [
    path('ip-info.json', ip_info, name='ip_info'),
]
