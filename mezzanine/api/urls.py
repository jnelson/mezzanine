from __future__ import unicode_literals

from django.conf.urls import patterns, url, include
from mezzanine.api.views import UserList, UserDetail

urlpatterns = patterns("",
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)

urlpatterns += patterns("mezzanine.api.views",
    url(r'^users/$', UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', UserDetail.as_view()),
    url(r'^oauth2/', include('provider.oauth2.urls', namespace='oauth2')),
)

