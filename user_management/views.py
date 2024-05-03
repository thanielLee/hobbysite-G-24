from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from .models import Profile
from .forms import CreateProfileView



# Create your views here.
class RegisterProfileView(CreateView):
    model = Profile
    form_class = CreateProfileView
    template_name = "registration/register.html"
    success_url = reverse_lazy("home")
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        user_profile = Profile.objects.get(user=user)
        user_profile.email = form.cleaned_data.get('email')
        user_profile.display_name = form.cleaned_data.get('display_name')
        user_profile.save()
        user.save()
        login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")
        return response

class UpdateProfileView(UpdateView):
    model = Profile
    fields = ['display_name', 'email']
    template_name = "update_profile.html"
    success_url = reverse_lazy("home")
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user_profile = form.save()
        user = user_profile.user
        user.email = form.cleaned_data.get('email')
        user.save()
        user_profile.save()
        return response