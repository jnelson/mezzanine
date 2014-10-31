from __future__ import unicode_literals

from django.conf.urls import patterns, url, include
from views import PagesAPIView


urlpatterns = patterns("",
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)

urlpatterns += patterns("mezzanine.api.views",
    url('^pages/$', PagesAPIView.as_view(), name='pages_api'),
)