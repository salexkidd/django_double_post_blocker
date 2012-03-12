from django.forms import ModelForm
from exampleapp.models import Whisper

class WhisperForm(ModelForm):
    class Meta(object):
        model = Whisper
        exclude = ['created_at']
