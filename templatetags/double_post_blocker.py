#-*- coding:utf-8 -*-

from django import template
from django.template.defaulttags import URLNode
from django.utils.safestring import mark_safe
from django.conf import settings

from random import randint
from time import time
import hashlib
import logging


register = template.Library()
logger = logging.getLogger('console.debug')


class DoublePostBlockerTokenNode(template.Node):
    """
    テンプレートに埋め込まれた{% double_post_blocker_token %}タグをレンダリングします
    """
    def render(self, context):
        user = context.get('user', None)
        dpb_token = hashlib.md5(
            "%s-%s-%s" % (time(), "%08s" % randint(0, 10000000), user.username)
            ).hexdigest()

        if dpb_token:
            if double_post_blocker_token == 'NOTPROVIDED':
                return mark_safe(u"")
            else:
                return mark_safe(
                    u"<div style='display:none'><input type='hidden' name='dpb_token' value='%s' /></div>" % dpb_token)
        else:
            from django.conf import settings
            if settings.DEBUG:
                import warnings
                warnings.warn("A {% double_post_blocker_token %} was used in a template, but the context did not provide the value.  This is usually caused by not using RequestContext.")
            return u''


def double_post_blocker_token(parser, token):
    """
    二重投稿を防止するためのトークンを埋め込むためのテンプレートタグを提供します
    {% double_post_blocker %}
    """
    return DoublePostBlockerTokenNode()
register.tag(double_post_blocker_token)
