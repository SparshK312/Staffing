from django import forms
from .models import Waitlist


class WaitlistForm(forms.ModelForm):
    class Meta:
        model = Waitlist
        fields = ["email"]


class AIRequestStep1Form(forms.ModelForm):
    class Meta:
        model = Waitlist
        fields = ["phone_number"]


class AIRequestStep2Form(forms.ModelForm):
    class Meta:
        model = Waitlist
        fields = ["email"]
