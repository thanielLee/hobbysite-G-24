from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Post, PostCategory

# Create your views here.
class ThreadListView(ListView):
    model = PostCategory
    template_name = 'forum_post_listview.html'

class ThreadDetailView(DetailView):
    model = Post
    template_name = 'forum_post_detailview.html'