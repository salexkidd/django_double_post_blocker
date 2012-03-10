import datetime
from django.db import models

class Whisper(models.Model):
    """Like a tweet, but quieter."""
    author = models.CharField(max_length=50)
    body = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True,
        default=datetime.datetime.utcnow(),
        editable=False,
    )
