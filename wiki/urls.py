from django.urls import path
from django.contrib import admin
from .views import WikiListView, WikiDetailView, WikiCreateView, WikiUpdateView

urlpatterns = [
    path('articles', WikiListView.as_view(), name='article-list'),
    path('article/<int:pk>', WikiDetailView.as_view(), name='article-detail'),
    path('article/add', WikiCreateView.as_view(), name = 'article-create'),
    path('article/<int:pk>/edit', WikiUpdateView.as_view(), name = 'article-update')]

app_name = 'wiki'