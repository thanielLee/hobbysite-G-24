from typing import Any
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Commission
from .forms import CommissionForm
from django.urls import reverse_lazy

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
        

class CommissionDetailView(DetailView):
    model = Commission
    template_name = 'commission_detail.html'

    

class CommissionCreateView(CreateView):
    model = Commission
    form_class = CommissionForm
    template_name = 'commission_createview.html'
    
    def get_success_url(self):
        return reverse_lazy('commissions:commission_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user.Profile
        return super().form_valid(form)
    
    
    
    
    
