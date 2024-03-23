from django.db import models
from django.utils import timezone


class Waitlist(models.Model):
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    ai_request = models.BooleanField(default=False)  # To identify if it's an AI request

    def __str__(self):
        return self.email
