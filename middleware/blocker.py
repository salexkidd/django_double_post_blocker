#-*- coding:utf-8 -*-

from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse as url_reverse


REDICECT_URL = "http://www.google.com"
CACHE_TIME = 7200


class DoublePostBlockerMiddleware:
    """
    POSTにて一緒に投げられた{% dpb_token %}(生成されたmd5値)を一時的にキャッシュし、
    同じdbp_tokenキーをもったPOSTがきたら無視する

    このmiddlewareを利用する場合は
    1.django.middleware.csrf.CsrfViewMiddlewareを組み込んでください
    2.POSTを行う場合は {% dbp_token %} をテンプレートに記述してください
    """
    def process_request(self, request):
        if request.method == "POST":
            if "dpb_token" in request.POST:
                if cache.get(request.POST['dpb_token']):
                    url = url_reverse('list_diary')
                    return HttpResponseRedirect(REDICECT_URL)
                else:
                    cache_key = request.POST['dpb_token']
                    cache.set(cache_key, 1, CACHE_TIME)
            else:
        return None
