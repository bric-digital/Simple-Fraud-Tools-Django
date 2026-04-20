# pylint: disable=line-too-long, wrong-import-position

import sys

if sys.version_info[0] > 2:
    from django.urls import re_path as url # pylint: disable=no-name-in-module
else:
    from django.conf.urls import url

from .views import ip_info

urlpatterns = [
    url('^ip-info.json$', ip_info, name='ip_info'),
]
