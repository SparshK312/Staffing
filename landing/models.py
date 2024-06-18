from django.db import models
from django.utils import timezone

class DemoUsage(models.Model):
    phone_number = models.CharField(max_length=15)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.phone_number} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
    

class Waitlist(models.Model):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    company_name = models.CharField(max_length=100, blank=True)  # Making it optional
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    ai_request = models.BooleanField(default=False)  # To identify if it's an AI request

    def __str__(self):
        return self.email
