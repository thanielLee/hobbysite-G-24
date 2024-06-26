from typing import Any
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from .models import Commission, Job, JobApplication
from .forms import CommissionForm, JobApplicationForm, JobCreationFormSet, JobApplicationUpdateForm, JobApplicationFormSet, JobApplicationUpdateFormSet, JobUpdateFormSet, JobUpdateForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from django.forms import formset_factory
from user_management.models import Profile
import django.contrib.messages as messages
from django.contrib.auth.decorators import login_required
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
            commission_id_set = set()
            
            user_job_applications = list(JobApplication.objects.filter(applicant=user.Profile))
            for job_application in user_job_applications:
                cur_job = job_application.job
                cur_commission = cur_job.commission
                commission_id_set.add(cur_commission.id)
            user_applied_commissions = []
            for commission_id in commission_id_set:
                user_applied_commissions.append(Commission.objects.get(id=commission_id))
            data['user_applied'] = user_applied_commissions
            
            return data
        else:
            return super().get_context_data(**kwargs)

class CommissionTemplateUpdateView(TemplateView):
    template_name = 'commission_updateview.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        commission = get_object_or_404(Commission, id=self.kwargs["commission_pk"])
        new_jobs = JobCreationFormSet(queryset=Job.objects.none())

        data = {
            'title' : commission.title,
            'description' : commission.description,
            'status' : commission.status
        }
        commission_form = CommissionForm(data=data)
        commission_jobs = Job.objects.filter(commission=commission)
        job_formset = []
        error = 0
        
        if 'form' in kwargs.keys():
            commission_form = kwargs['form']
            
        if 'new_jobset' in kwargs.keys():
            new_jobs = kwargs['new_jobset']
                
        if 'with_error' in kwargs.keys():
            error = kwargs['with_error']

        test = []
        job_application_forms = []
        job_applications = []
        for job in commission_jobs:
            job_application_formset = JobApplication.objects.filter(job=job)
            job_form = JobUpdateForm(instance=job)
            job_formset.append(job_form)
            for job_application in job_application_formset:
                new_form = JobApplicationUpdateForm(instance=job_application)
                job_application_forms.append(new_form)
                job_applications.append(job_application)
        
        data['form'] = commission_form
        data['job_formset'] = job_formset
        data['with_error'] = error
        data['job_application_forms'] = job_application_forms
        data['job_applications'] = job_applications
        data['new_jobs'] = new_jobs
        data['jobs'] = commission_jobs
        return data 
    
    def get_success_url(self, pk):

        return reverse('commissions:commission_detail', kwargs={'pk':pk})
    
    def form_valid(self, request, form, job_formset, cur_commission):
        for job_form in job_formset:
            if 'role' not in job_form.cleaned_data.keys() and 'manpower_required' not in job_form.cleaned_data.keys():
                        continue
            job_form.instance.commission_id = cur_commission.id
        job_formset.save()
        return redirect(self.get_success_url(cur_commission.id))
    
    def form_invalid(self, form, job_formset, error):
        return self.render_to_response(self.get_context_data(form=form, new_jobset=job_formset, with_error=error))

    def post(self, request, *args, **kwargs):
        ctx = self.get_context_data(**kwargs)
        test_dict = dict(request.POST)
        commission_form = CommissionForm(data=request.POST)
        cur_commission = Commission.objects.get(id=int(kwargs['commission_pk']))
        create_formset = JobUpdateFormSet(data=request.POST)
        counter = 0
        while counter < len(ctx['jobs']):
            cur_job = ctx['jobs'][counter]
            cur_job.role = test_dict['role'][counter]
            cur_job.manpower_required = test_dict['manpower_required'][counter]
            cur_job.save()
            if cur_job.current_manpower > int(test_dict['manpower_required'][counter]):
                return self.form_invalid(commission_form, create_formset, 2)

            counter += 1
        
        counter = 0
        while counter < len(ctx['job_applications']):
            cur_job_application = ctx['job_applications'][counter]
            cur_job_application.application_status = test_dict['application_status'][counter]
            counter += 1
            cur_job_application.save()
        
        
        formset = create_formset
        if commission_form.is_valid():
            cur_commission.title = commission_form.cleaned_data['title']
            cur_commission.description = commission_form.cleaned_data['description']
            cur_commission.save()
            
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    if 'role' not in form.cleaned_data.keys() and 'manpower_required' not in form.cleaned_data.keys():
                        continue
                    if 'role' not in form.cleaned_data.keys() or 'manpower_required' not in form.cleaned_data.keys():
                        return self.form_invalid(commission_form, formset, 1)
                else:
                    return self.form_invalid(commission_form, formset, 1)
                
            return self.form_valid(request, commission_form, formset, cur_commission)
        
        return self.form_invalid(commission_form, formset, 1)
        
class CommissionTemplateDetailView(TemplateView):
    template_name = 'commission_detail.html'

    def dispatch(self, request, *args, **kwargs):
        job_application_data = request.session.get('temp_form')
        if job_application_data:
            new_form = JobApplicationForm()
            new_job_application = new_form.save(commit=False)
            user = self.request.user
            new_job_application.job = Job.objects.get(id=job_application_data['job'])
            new_job_application.applicant = user.Profile
            new_job_application.save()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        commission = Commission.objects.get(id=data['pk'])
        total_manpower_required = 0
        commission_current_manpower = 0
        job_set = Job.objects.filter(commission=commission)
        formset = formset_factory(JobApplicationForm)
        job_applied_by_user = []
        print(commission.get_status_display())

        STATUS_CHOICES = {
            "0": "Pending",
            "1": "Accepted",
            "2": "Rejected"
        }
        
        for job in job_set:
            job_application_set = JobApplication.objects.filter(job = job)
            total_manpower_required += job.manpower_required
            current_job_manpower = 0
            for job_application in job_application_set:
                if job_application.application_status == "1": 
                    commission_current_manpower += 1
                    current_job_manpower += 1
            
            job.modify_current_manpower(current_job_manpower)
            job.open_manpower =  job.manpower_required - current_job_manpower
            if job.open_manpower == 0:
                job.status = "2"      
        
        test = []
        for job in job_set:
            cur_queryset = JobApplication.objects.filter(job=job)
            for job_app in cur_queryset:
                if job_app.applicant == self.request.user.Profile:
                    job_applied_by_user.append(job)
            new_form = JobApplicationForm()
            if job.open_manpower > 0:
                submit = 1
            else:
                submit = 0
            test.append([job, new_form, submit, job.id])
            
        data['object'] = commission
        data['jobs'] = test
        data['total_manpower_required'] = total_manpower_required
        data['current_manpower'] = commission_current_manpower
        data['open_manpower'] = total_manpower_required-commission_current_manpower
        data['commission_owner'] = commission.created_by.id
        data['jobs_applied_by_user'] = job_applied_by_user
        data['status_choice'] = STATUS_CHOICES
        if total_manpower_required-commission_current_manpower == 0:
            commission.status = "2"
        return data

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.request.path_info)
    
    def post(self, request, *args, **kwargs):
        cur_job = Job.objects.get(id=int(request.POST['hidden_job_id']))
        cur_data = request.POST.copy()
        cur_data['job'] = cur_job
        if not self.request.user.is_authenticated:
            request.session['temp_form'] = {
                'job' : cur_job.id
            }
            login_url = reverse('login') + '?next=' + request.get_full_path()
            return redirect(login_url)
        
        cur_data['applicant'] = self.request.user.Profile
        job_application_form = JobApplicationForm(cur_data)
        if job_application_form.is_valid():
            return self.form_valid(job_application_form)
        else:
            return self.form_invalid(job_application_form)
        
    def get_success_url(self) -> str:
        return reverse_lazy('commissions:commission_list')


def test(**kwargs):
    kwargs['won'] = 2
test(won=2) 
class CommissionCreateViewTemplate(TemplateView):
    template_name = 'commission_createview.html'
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        commission_form = CommissionForm()
        job_formset = JobCreationFormSet(queryset=Job.objects.none())
        error = 0
        
        if 'form' in kwargs.keys():
            commission_form = kwargs['form']
            
        if 'job_formset' in kwargs.keys():
            job_formset = kwargs['job_formset']
        
        if 'with_error_incomplete' in kwargs.keys():
            error = kwargs['with_error_incomplete']

        data['form'] = commission_form
        data['job_formset'] = job_formset
        data['with_error'] = error
        return data
    
    def get_success_url(self, pk):

        return reverse('commissions:commission_detail', kwargs={'pk':pk})
    
    def form_valid(self, request, form, job_formset):
        form.instance.created_by = request.user.Profile     
        form.save()
        for job_form in job_formset:
            if 'role' not in job_form.cleaned_data.keys() and 'manpower_required' not in job_form.cleaned_data.keys():
                        continue
            job_form.instance.commission_id = form.instance.id
        job_formset.save()
        return redirect(self.get_success_url(form.instance.id))
    
    def form_invalid(self, form, job_formset):
        return self.render_to_response(self.get_context_data(form=form, job_formset=job_formset, with_error=1))

    def post(self, request, *args, **kwargs):
        commission_form = CommissionForm(data=request.POST)
        formset = JobCreationFormSet(data=request.POST)
        
        if formset.is_valid() and commission_form.is_valid():
            for form in formset:
                if form.is_valid():
                    if 'role' not in form.cleaned_data.keys() and 'manpower_required' not in form.cleaned_data.keys():
                        continue
                    if 'role' not in form.cleaned_data.keys() or 'manpower_required' not in form.cleaned_data.keys():
                        return self.form_invalid(commission_form, formset)
                else:
                    return self.form_invalid(commission_form, formset)
                
            return self.form_valid(request, commission_form, formset)
        
        return self.form_invalid(commission_form, formset)