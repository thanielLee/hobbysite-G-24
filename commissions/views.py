from typing import Any
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, ModelFormMixin, UpdateView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Commission, Job, JobApplication
from .forms import CommissionForm, JobApplicationForm, JobCreationFormSet
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.forms import formset_factory
from user_management.models import Profile
import datetime

def index(request):
    return HttpResponse("Commissions App")

class CommissionListView(ListView):
    model = Commission
    template_name = 'commission_list.html'
    
    def get_context_data(self, **kwargs: Any):
        user = self.request.user
        if user.is_authenticated:
            data = super().get_context_data(**kwargs)
            data['user_created'] = Commission.objects.filter(created_by=user.Profile)
            
            return data
        else:
            return super().get_context_data(**kwargs)
        

class CommissionDetailView(ModelFormMixin, DetailView):
    model = Commission
    template_name = 'commission_detail.html'
    form_class = JobApplicationForm
    

    def get_context_data(self, **kwargs):
        commission = self.get_object()
        total_manpower_required = 0
        commission_current_manpower = 0
        job_set = Job.objects.filter(commission=commission)
        formset = formset_factory(JobApplicationForm)
        for job in job_set:
            job_application_set = JobApplication.objects.filter(job = job)
            total_manpower_required += job.manpower_required
            current_job_manpower = 0
            for job_application in job_application_set:
                if job_application.status == 1: 
                    commission_current_manpower += 1
                    current_job_manpower += 1
            
            job.modify_current_manpower(current_job_manpower)
            job.open_manpower =  job.manpower_required - current_job_manpower
            if job.open_manpower == 0:
                job.status = 2      
        
        data = super().get_context_data(**kwargs)
        
        cnt = 0
        test = []
        for job in job_set:
            new_form = JobApplicationForm()
            test.append([job, new_form])
            
        
        data['jobs'] = test
        data['total_manpower_required'] = total_manpower_required
        data['current_manpower'] = commission_current_manpower
        data['open_manpower'] = total_manpower_required-commission_current_manpower
        data['commission_owner'] = commission.created_by.id
        if total_manpower_required-commission_current_manpower == 0:
            commission.status = 2
        return data
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form.instance.applicant = Profile.objects.get(id=int(form['applicant'].value()))
        form.instance.job = Job.objects.get(id=int(form['job'].value()))
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def get_success_url(self) -> str:
        return reverse_lazy('commissions:commission_list')
    
class CommissionCreateView(CreateView):
    model = Commission
    form_class = CommissionForm
    template_name = 'commission_createview.html'
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        job_formset = JobCreationFormSet(queryset=Job.objects.none())
        data['job_formset'] = job_formset
        return data
    
    def get_success_url(self):
        return reverse_lazy('commissions:commission_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user.Profile
        return super().form_valid(form)
    
    def post(self, *args, **kwargs):
        formset = JobCreationFormSet(data=self.request.POST)
        
        if formset.is_valid():
            formset.save()
            return redirect(reverse_lazy('commissions:commission_list'))    
        
        return self.render_to_response({'job_formset': formset})

    
