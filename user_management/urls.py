from django.urls import path
from .views import RegisterProfileView

urlpatterns = [
    path('register/', RegisterProfileView.as_view(), name='register'),
] 

app_name = 'user_management'