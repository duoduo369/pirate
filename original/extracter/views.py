# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from common import constants, exceptions, tools
from django.shortcuts import render
from django_validator.decorators import GET, POST
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import WXArticle


class WXArticleListAPI(APIView):

    @POST('raw_url', type='str', validators='required')
    def post(self, request, raw_url):
        if not raw_url.startswith('https://mp.weixin.qq.com/') and not raw_url.startswith('http://mp.weixin.qq.com/'):
            raise exceptions.APIException(message='只能抓取微信类文章')
        article = WXArticle.new_article(raw_url)
        return Response()
