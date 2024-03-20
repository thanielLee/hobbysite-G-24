from django.urls import path
from django.contrib import admin
from .views import WikiListView, WikiDetailView

urlpatterns = [
    path('articles', WikiListView.as_view(), name='article-list'),
    path('article/<int:pk>', WikiDetailView.as_view(), name='article-detail')]

app_name = 'wiki'