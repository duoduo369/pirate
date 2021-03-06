# -*- coding: utf-8 -*-
import uuid
import requests
import pyqrcode
from StringIO import StringIO

from .data_structure import ObjectDict
from .upload import upload_handler


def qrcode(text):
    scale = 6
    q = pyqrcode.create(text)
    return 'data:image/png;base64,{}'.format(q.png_as_base64_str(scale))


def iter_items(items, interval, total=None):
  """
  :param items: 要遍历的集合
  :param interval: 每次遍历的元素的数量
  :return:
  """
  if interval < 1:
      return

  start = 0
  if total is None:
      total = len(items)
  while True:
      if start >= total:
          break
      yield items[start:start + interval]
      start += interval


def format_api_object(obj, attrs):
    result = ObjectDict()
    for attr in attrs:
        result[attr] = getattr(obj, attr)
    return result


def get_result_in_query_order(query_set, query_ids, query_key='id'):
    mapper = {getattr(each, query_key):each for each in query_set}
    result = []
    for _id in query_ids:
        if _id in mapper:
            result.append(mapper[_id])
    return result


def spider_request(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }
    resp = requests.get(url, timeout=10, headers=headers)
    if resp.status_code >= 300 or resp.status_code < 200:
        logging.warning('[spider_request] failed %s', resp.content)
        return ''
    else:
        return resp.content


def upload_file_from_url(url, upload_file_name=None, suffix=None):
    result = {
        'raw_url': url,
        'url': '',
    }
    if suffix is None:
        if url.endswith('gif'):
            suffix = 'gif'
        elif url.endswith('jpg') or url.endswith('jpeg'):
            suffix = 'jpg'
        else:
            suffix = 'png'

    if not upload_file_name:
        upload_file_name = '{}.{}'.format(uuid.uuid4().hex[:12], suffix)
    try:
        resp = requests.get(url, timeout=10)
    except Exception as ex:
        logging.error('[upload_file_from_url] failed %s', url, exc_info=1)
        return result
    if resp.status_code != 200:
        return result
    file_obj = StringIO(resp.content)
    upload_resp = upload_handler.upload_file(upload_file_name, file_obj)
    result['url'] = upload_handler.get_download_url(upload_file_name)
    return result
