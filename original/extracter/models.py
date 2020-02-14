# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bs4 import BeautifulSoup
from common import tools
from django.db import models
from jsonfield import JSONField
from model_utils import Choices
from model_utils.models import TimeStampedModel
from misc.models import URLFileUploadCache


class WXArticle(TimeStampedModel):
    raw_url = models.CharField(max_length=1023)
    title = models.CharField(max_length=255)
    cover = models.CharField(max_length=255)
    description = models.CharField(max_length=255, default='')
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    @classmethod
    def spider_url(cls, raw_url):
        assert raw_url.startswith('https://mp.weixin.qq.com/') or raw_url.startswith('http://mp.weixin.qq.com/')
        content = tools.spider_request(raw_url)
        description = content_text = title = cover = ''
        body_script = ''
        if content:
            b = BeautifulSoup(content, 'html.parser')
            content_dom = b.find('div', id='js_content')
            title_dom = b.find('meta', property="og:title")
            cover_dome = b.find('meta', property="og:image")
            if title_dom:
                title = title_dom.attrs['content']
            if cover_dome:
                cover = cover_dome.attrs['content']
                raw_url = cover
                upload_cache = URLFileUploadCache.get_cached_objects(raw_url, get_last=True)
                if upload_cache:
                    cover = upload_cache[0].url
                else:
                    upload_data = tools.upload_file_from_url(raw_url)
                    url = upload_data['url']
                    if url:
                        URLFileUploadCache.new_cache(raw_url, url)
                        cover = url
            if content_dom:
                content_text = unicode(content_dom)
                ss = b.body.find_all('script')
                body_script = ''.join(unicode(s) for s in ss)
                urls = []
                for _re in constants.WEIXIN_IMAGE_RES:
                    urls.extend(_re.findall(content_text))
                descriptions = constants.WEIXIN_DESCRIPTION_RE.findall(content)
                if descriptions:
                    description = BeautifulSoup(descriptions[0]).meta.attrs.get('content', '')
                mapper = {}
                for raw_url in urls:
                    if raw_url in mapper:
                        continue
                    upload_cache = URLFileUploadCache.get_cached_objects(raw_url, get_last=True)
                    if upload_cache:
                        mapper[raw_url] = upload_cache[0].url
                    else:
                        upload_data = tools.upload_file_from_url(raw_url, )
                        url = upload_data['url']
                        if url:
                            URLFileUploadCache.new_cache(raw_url, url)
                            mapper[raw_url] = url
                for raw_url, url in mapper.iteritems():
                    if not url:
                        continue
                    content_text = content_text.replace(raw_url, url)
        return {
            'raw_url': raw_url,
            'title': title,
            'cover': cover,
            'content': content_text,
            'description': description,
            'body_script': body_script,
        }

    @classmethod
    def new_article(cls, raw_url):
        data = cls.spider_url(raw_url)
        title = data['title']
        cover = data['cover']
        raw_content = data['content']
        description = data['description']
        body_script = data['body_script']
        article = cls.objects.create(
            raw_url=raw_url, title=title, cover=cover, is_active=True, description=description
        )
        content = CustomerArticleContent.objects.create(article_id=article.id, content=raw_content, body_script=body_script)
        article.content = content
        return article


class WXArticleContent(TimeStampedModel):
    article_id = models.IntegerField(unique=True)
    content = models.TextField()
    body_script = models.TextField(default='')
