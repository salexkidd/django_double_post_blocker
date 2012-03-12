#-*- coding:utf-8 -*-

from random import randint
from time import time
import hashlib
import logging

from django import template
from django.utils.safestring import mark_safe


register = template.Library()
logger = logging.getLogger('console.debug')


class DoublePostBlockerTokenNode(template.Node):
    """
    Renders {% double_post_blocker_token %} template tag.
    テンプレートに埋め込まれた{% double_post_blocker_token %}
    タグをレンダリングします
    """
    def render(self, context):
        user = context.get('user', None)
        username = user.username
        dpb_token = hashlib.md5(
            "%s-%s-%s" % (time(), "%08s" % randint(0, 10000000), username)
            ).hexdigest()

        if dpb_token:
            if double_post_blocker_token == 'NOTPROVIDED':
                return mark_safe(u"")
            else:
                return mark_safe(
                    u"<div style='display:none'>"
                    "<input type='hidden' name='dpb_token' value='%s' />"
                    "</div>" % dpb_token)
        else:
            from django.conf import settings
            if settings.DEBUG:
                import warnings
                warnings.warn(
                    "A {% double_post_blocker_token %} was used in a "
                    "template, but the context did not provide the value. "
                    "This is usually caused by not using RequestContext.")
            return u''


def double_post_blocker_token(parser, token):
    """
    Return HTML with hidden input containing double post blocker token.
    二重投稿を防止するためのトークンを埋め込むための
    テンプレートタグを提供します
    {% double_post_blocker %}
    """
    return DoublePostBlockerTokenNode()

register.tag(double_post_blocker_token)
