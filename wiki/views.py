from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Article


class WikiListView(ListView):
	model = Article  
	template_name = "wiki_article_category_list.html"

class WikiDetailView(DetailView):
	model = Article
	template_name = "wiki_article_detail.html"