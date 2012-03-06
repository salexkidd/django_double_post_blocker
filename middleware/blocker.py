#-*- coding:utf-8 -*-

from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse as url_reverse

import logging
logger = logging.getLogger('console.debug')


class DoublePostBlockerMiddleware:
    """
    POSTにて一緒に投げられたCSRFを一時的にキャッシュし、同じCSRFキーをもったPOSTがきたら無視する

    このmiddlewareを利用する場合は
    1.django.middleware.csrf.CsrfViewMiddlewareを組み込んでください
    2.POSTを行う場合は {% csrf_token %} をテンプレートに記述してください
    """
    def process_request(self, request):
        if request.method == "POST":
            if "dpb_token" in request.POST:
                if cache.get(request.POST['dpb_token']):
                    url = url_reverse('list_diary')
                    logger.debug("Cache has same csrf token. double post")
                    return HttpResponseRedirect(url)
                else:
                    cache_key = request.POST['dpb_token']
                    cache.set(cache_key, 1, 7200)
            else:
                logger.debug("dpb_token not found.")
        return None
