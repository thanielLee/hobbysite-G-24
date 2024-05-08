from django.urls import path
from .views import ThreadListView, ThreadDetailView, ThreadCreateView, ThreadEditView

urlpatterns = [
    path('threads', ThreadListView.as_view(), name='thread-list'),
    path('thread/<int:pk>', ThreadDetailView.as_view(), name='thread-detail'),
    path('thread/add', ThreadCreateView.as_view(), name='thread-create'),
    path('thread/<int:pk>/edit', ThreadEditView.as_view(), name='thread-edit')
]

app_name = "forum"