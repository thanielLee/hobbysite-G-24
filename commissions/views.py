from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Commission

def index(request):
    return HttpResponse("Commissions App")

class CommissionListView(ListView):
    model = Commission
    template_name = 'commission_list.html'

class CommissionDetailView(DetailView):
    model = Commission
    template_name = 'commission_detail.html'

