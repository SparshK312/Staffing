from django.db import models

class Waitlist(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    company_name = models.CharField(max_length=100, blank=True)  # Making it optional
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    ai_request = models.BooleanField(default=False)  # To identify if it's an AI request

    def __str__(self):
        return self.email
