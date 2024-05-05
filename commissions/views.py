from typing import Any
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, ModelFormMixin, UpdateView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Commission, Job, JobApplication
from .forms import CommissionForm, JobApplicationForm, JobCreationFormSet, JobApplicationFormSet
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
            
            return data
        else:
            return super().get_context_data(**kwargs)

class CommissionTemplateUpdateView(TemplateView):
    template_name = 'commission_updateview.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        commission = get_object_or_404(Commission, id=self.kwargs["commission_pk"])

        data = {
            'title' : commission.title,
            'description' : commission.description,
            'status' : commission.status
        }
        commission_form = CommissionForm(data=data)
        job_formset = JobCreationFormSet(queryset=Job.objects.filter(commission=commission))
        error = 0
        if 'form' in kwargs.keys():
            commission_form = kwargs['form']
            
        if 'job_formset' in kwargs.keys():
            job_formset = kwargs['job_formset']
        
        if 'with_error' in kwargs.keys():
            error = kwargs['with_error']
        print(job_formset)
        data['form'] = commission_form
        data['job_formset'] = job_formset
        data['with_error'] = error
        return data
    
    def get_success_url(self):
        return reverse_lazy('commissions:commission_list')
    
    def form_valid(self, request, form, job_formset):
        form.instance.created_by = request.user.Profile     
        form.save()
        for job_form in job_formset:
            if 'role' not in job_form.cleaned_data.keys() and 'manpower_required' not in job_form.cleaned_data.keys():
                        continue
            job_form.instance.commission_id = form.instance.id
        job_formset.save()
        return redirect(self.get_success_url())
    
    def form_invalid(self, form, job_formset):
        messages.error(self.request, "Please fill in empty data")
        print("WRONG")
        return self.render_to_response(self.get_context_data(form=form, job_formset=job_formset, with_error=1))

    def post(self, request, *args, **kwargs):
        commission_form = CommissionForm(data=request.POST)
        formset = JobCreationFormSet(data=request.POST)
        
        if formset.is_valid() and commission_form.is_valid():
            for form in formset:
                print(form.data)
                if form.is_valid():
                    if 'role' not in form.cleaned_data.keys() and 'manpower_required' not in form.cleaned_data.keys():
                        continue
                    if 'role' not in form.cleaned_data.keys() or 'manpower_required' not in form.cleaned_data.keys():
                        return self.form_invalid(commission_form, formset)
                else:
                    return self.form_invalid(commission_form, formset)
                
            return self.form_valid(request, commission_form, formset)
        
        return self.form_invalid(commission_form, formset)
        
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

        STATUS_CHOICES = {
            0: "Pending",
            1: "Accepted",
            2: "Rejected"
        }
        
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
        
        test = []
        for job in job_set:
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
        print(job_applied_by_user)
        data['status_choice'] = STATUS_CHOICES
        if total_manpower_required-commission_current_manpower == 0:
            commission.status = 2
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
        print(cur_data)
        job_application_form = JobApplicationForm(cur_data)
        print(self.request.user.Profile.id, cur_job.id)
        print(job_application_form.data)
        print(job_application_form)
        print("yes", job_application_form.is_valid())
        if job_application_form.is_valid():
            return self.form_valid(job_application_form)
        else:
            return self.form_invalid(job_application_form)
        
    def get_success_url(self) -> str:
        return reverse_lazy('commissions:commission_list')
    
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
        
        if 'with_error' in kwargs.keys():
            error = kwargs['with_error']
        data['form'] = commission_form
        data['job_formset'] = job_formset
        data['with_error'] = error
        return data
    
    def get_success_url(self):
        return reverse_lazy('commissions:commission_list')
    
    def form_valid(self, request, form, job_formset):
        form.instance.created_by = request.user.Profile     
        form.save()
        for job_form in job_formset:
            if 'role' not in job_form.cleaned_data.keys() and 'manpower_required' not in job_form.cleaned_data.keys():
                        continue
            job_form.instance.commission_id = form.instance.id
        job_formset.save()
        return redirect(self.get_success_url())
    
    def form_invalid(self, form, job_formset):
        messages.error(self.request, "Please fill in empty data")
        print("WRONG")
        return self.render_to_response(self.get_context_data(form=form, job_formset=job_formset, with_error=1))

    def post(self, request, *args, **kwargs):
        commission_form = CommissionForm(data=request.POST)
        formset = JobCreationFormSet(data=request.POST)
        
        if formset.is_valid() and commission_form.is_valid():
            for form in formset:
                print(form.data)
                if form.is_valid():
                    if 'role' not in form.cleaned_data.keys() and 'manpower_required' not in form.cleaned_data.keys():
                        continue
                    if 'role' not in form.cleaned_data.keys() or 'manpower_required' not in form.cleaned_data.keys():
                        return self.form_invalid(commission_form, formset)
                else:
                    return self.form_invalid(commission_form, formset)
                
            return self.form_valid(request, commission_form, formset)
        
        return self.form_invalid(commission_form, formset)
    
    
"""class CommissionCreateView(CreateView):
    model = Commission
    form_class = CommissionForm
    template_name = 'commission_createview.html'
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)
    
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
    
    def form_invalid(self, form):
        messages.error(self.request, "Please fill in empty data")
        print("WRONG")
        return self.render_to_response(self.get_context_data(form=form))
    
    def post(self, request, *args, **kwargs):
        commission_form = super(CommissionCreateView, self).get_form()
        formset = JobCreationFormSet(request.POST, request.FILES)
        
        if formset.is_valid() and commission_form.is_valid():
            for form in formset:
                if form.is_valid():
                    form.instance.commission_id = commission_form.instance.id
                    if 'role' not in form.cleaned_data.keys() or 'manpower_required' not in form.cleaned_data.keys():
                        print('oopsie')
                        return self.form_invalid(commission_form)
                else:
                    return self.form_invalid(commission_form)
                
            formset.save()
            print("WHYMAN")
            return self.form_valid(commission_form)
        
        print("why", commission_form)
        return self.form_invalid(commission_form)
        
        
        
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
        return reverse_lazy('commissions:commission_list')"""

    
