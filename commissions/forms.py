from django import forms

from .models import Commission, JobApplication, Job
from django.forms import HiddenInput, modelformset_factory

class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = ['title', 'description', 'status']

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = "__all__"
        exclude = ["status"]
        widgets = {'job': HiddenInput(), 'applicant': HiddenInput()} 

class JobCreationForm(forms.ModelForm):
    role = forms.CharField(required=True, max_length=255)
    manpower_required = forms.IntegerField(required=True)
    
    
    class Meta:
        model = Job
        fields = ['role', 'manpower_required', 'status']

JobCreationFormSet = modelformset_factory(
    Job,
    form = JobCreationForm,
    extra=1
)

JobApplicationFormSet = modelformset_factory(
    JobApplication,
    form = JobApplicationForm
)