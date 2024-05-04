from django import forms

from .models import Commission, JobApplication
from django.forms import HiddenInput

class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = ['title', 'description', 'status']

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = "__all__"
        exclude = ["status"]
        widgets = {'job': HiddenInput(), 'applicant': HiddenInput(),}