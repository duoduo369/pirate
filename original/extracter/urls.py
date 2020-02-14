# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from . import views


api_urlpatterns = [
    url(r'^extrack/wx/$', views.WXArticleListAPI.as_view(), name='extrack_wxarticle'),
]

urlpatterns = [
    url(r'^api/v1/', include(api_urlpatterns, namespace='api.v1')),
]
