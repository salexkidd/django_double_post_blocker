#-*- coding:utf-8 -*-

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseRedirect


REDIRECT_URL = "/"
CACHE_TIME = 7200


class DoublePostBlockerMiddleware:
    """
    Checks {% double_post_blocker_token %} in template,
    redirects to DBP_REDIRECT_URL in project settings or
    domain index if duplicate with cached value.

    POSTにて一緒に投げられた{% double_post_blocker_token %}
    (生成されたmd5値)を一時的にキャッシュし、
    同じdbp_tokenキーをもったPOSTがきたら無視する

    このmiddlewareを利用する場合は
    1.settings.pyの"MIDDLEWARE_CLASSES"に
    "django_double_post_blocker.middleware.DoublePostBlockerMiddleware"
     を組み込んでください

    2.POSTを行うテンプレート中の<FORM>...</FORM>中に{% dbp_token %}を
    記述してください

    3. リダイレクト先のURLを静的なものに変更する場合settings.pyに以下を
    追加してください

    DPB_REDIRECT_URL = "http://[飛ばし先のURL]"
    """
    def process_request(self, request):
        if request.method == "POST":
            if "dpb_token" in request.POST:
                if cache.get(request.POST['dpb_token']):
                    redirect_url = REDIRECT_URL
                    if hasattr(settings, "DPB_REDIRECT_URL"):
                        redirect_url = settings.DPB_REDIRECT_URL
                    return HttpResponseRedirect(redirect_url)
                else:
                    cache_key = request.POST['dpb_token']
                    cache.set(cache_key, 1, CACHE_TIME)
        return None
