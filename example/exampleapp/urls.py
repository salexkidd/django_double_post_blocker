from django.conf.urls.defaults import patterns, url
# from exampleapp.views import WhisperView

urlpatterns = patterns('',
    url(
        regex=r'^$',
        view='exampleapp.views.whisper',
        # view=WhisperView.as_view(),
        name='whisper'
    ),
)
