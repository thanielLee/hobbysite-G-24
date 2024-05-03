from django.urls import path
from .views import RegisterProfileView, UpdateProfileView

urlpatterns = [
    path('register/', RegisterProfileView.as_view(), name='register'),
    path('<int:pk>/', UpdateProfileView.as_view(), name='update')
] 

app_name = 'user_management'