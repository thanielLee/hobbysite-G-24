from django.urls import path
from .views import ThreadListView, ThreadDetailView

urlpatterns = [
    path('threads', ThreadListView.as_view(), name='thread-list'),
    path('thread/<int:pk>', ThreadDetailView.as_view(), name='thread-detail')
]

app_name = "forum"