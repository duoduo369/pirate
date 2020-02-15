# -*- coding: utf-8 -*-
import re
from enum import Enum, IntEnum, unique

DEFAULT_LIMIT = 20
VALIDATION_SESSION_KEY = 'verify'
WEIXIN_IMAGE_RES = [
    re.compile(r'''https://mmbiz.qpic.cn/mmbiz_[^\? '"]*\?wx_fmt=(?:jpeg|png|gif)'''),
    re.compile(r'''https://mmbiz.qpic.cn/mmbiz_(?:jpe?g|png|gif)/\w+/\d+''')
]
WEIXIN_DESCRIPTION_RE = re.compile(r'<meta name="description" content="[\S]*" />')


def get_key_by_value(enum, value):
    for k, v in enum.__members__.iteritems():
        if v.value == value:
            return k


class IntEnumMixin(IntEnum):
    @classmethod
    def get_all_values(cls):
        return [each.value for each in cls.__members__.itervalues()]

    @classmethod
    def get_all_keys(cls):
        return cls.__members__.keys()

    @classmethod
    def get_all_values_string_format(cls, join_word=','):
        return join_word.join(map(str, cls.get_all_values()))
