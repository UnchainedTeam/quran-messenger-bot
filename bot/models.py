from django.db import models

class Message(models.Model):
    text = models.CharField(max_length=250)
    frequency = models.PositiveIntegerField(default=0)
    blacklist = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text