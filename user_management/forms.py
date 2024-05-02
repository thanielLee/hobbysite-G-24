from django.shortcuts import render
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Profile


class CreateProfileView(UserCreationForm):
    display_name = forms.CharField(max_length=63)
    email = forms.EmailField(required=False)
    
    class Meta:
        model = User
        fields = ["username", "display_name", "password1", "password2", "email"]


# Create your views here.
