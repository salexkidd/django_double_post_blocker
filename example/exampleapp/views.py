from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.views.generic import FormView
from django.template import RequestContext

from example.exampleapp.models import Whisper
from example.exampleapp.forms import WhisperForm

def whisper(request, template_name='exampleapp/whisper.html'):
    whisper_list = Whisper.objects.all().order_by('-created_at')
    if request.method == 'POST':
        form = WhisperForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = WhisperForm()
    return render_to_response(
        template_name, locals(), context_instance=RequestContext(request))



class WhisperView(FormView):
    """
    Generic form views always redirect on success,
    so they don't need django_double_post_blocker.
    See: https://github.com/django/django/blob/master/django/views/generic/edit.py#L59
    """
    template_name = 'exampleapp/whisper.html'

    def get_form_class(self):
        return WhisperForm

    def form_valid(self, form):
        form.save()
        return super(WhisperView, self).form_valid(form)

    def get_success_url(self):
        return reverse('whisper')

    def get_context_data(self, **kwargs):
        context = super(WhisperView, self).get_context_data(**kwargs)
        context['whisper_list'] = Whisper.objects.all()
        return context
