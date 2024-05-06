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
        exclude = ["application_status"]
        widgets = {'job': HiddenInput(), 'applicant': HiddenInput()} 

class JobApplicationUpdateForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = "__all__"

        widgets = {'job': HiddenInput(), 'job_application_id': HiddenInput()} 
    
    def __init__(self, *args, **kwargs):
        super(JobApplicationUpdateForm, self).__init__(*args, **kwargs)
        self.fields['applicant'].disabled = True


class JobCreationForm(forms.ModelForm):
    role = forms.CharField(required=True, max_length=255)
    manpower_required = forms.IntegerField(required=True)
    
    
    class Meta:
        model = Job
        fields = ['role', 'manpower_required']

class JobUpdateForm(forms.ModelForm):
    role = forms.CharField(required=True, max_length=255)
    manpower_required = forms.IntegerField(required=True)
    
    
    class Meta:
        model = Job
        fields = ['role', 'manpower_required']
        widgets = {'job_id':HiddenInput()}

JobCreationFormSet = modelformset_factory(
    Job,
    form = JobCreationForm,
    extra=1
)

JobUpdateFormSet = modelformset_factory(
    Job,
    form = JobUpdateForm,
)

JobApplicationFormSet = modelformset_factory(
    JobApplication,
    form = JobApplicationForm
)

JobApplicationUpdateFormSet = modelformset_factory(
    JobApplication,
    form = JobApplicationUpdateForm
)