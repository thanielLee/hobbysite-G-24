from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Article, ArticleCategory
from .forms import ArticleForm, CommentForm
from user_management import models as ProfileModel

class WikiListView(ListView):
	model = ArticleCategory
	template_name = "wiki_article_category_list.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.request.user.is_authenticated:
			author = ProfileModel.Profile.objects.get(user=self.request.user)
			context['articles_by_author'] = Article.objects.filter(article_author=author)
		return context
		
class WikiDetailView(DetailView):
	model = Article
	template_name = "wiki_article_detail.html"

	def get_context_data(self, **kwargs):	
		context = super().get_context_data(**kwargs)
		articles_by_author = self.get_object()
		if self.request.user.is_authenticated:
			author = ProfileModel.Profile.objects.get(user=self.request.user)
			context['viewer'] = author
			context['form'] = CommentForm()
			
		context['categories'] = Article.objects.filter(article_category=articles_by_author.article_category)
		return context
	
	def post(self, request, **kwargs):
		form = CommentForm(request.POST) 
		author = ProfileModel.Profile.objects.get(user=self.request.user)
		article = self.get_object()
		
		if form.is_valid():
			comment = form.save(commit=False)
			comment.comment_author_wiki = author
			comment.comment_article = article
			comment.save()
			return redirect('wiki:article-detail', pk=article.pk)
		context = self.get_context_data(**kwargs)
		return self.render_to_response(context)
	

class WikiCreateView(LoginRequiredMixin, CreateView):
	model = Article
	form_class = ArticleForm
	template_name = "wiki_article_create.html"

	def get_success_url(self):
		return reverse_lazy('wiki:article-detail', kwargs={'pk': self.object.pk})
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		author = ProfileModel.Profile.objects.get(user=self.request.user)
		context['form'] = ArticleForm(initial={'article_author': author})
		return context
	
	def get_initial(self):
		author = ProfileModel.Profile.objects.get(user=self.request.user)
		return{'article_author': author}


class WikiUpdateView(LoginRequiredMixin, UpdateView):
	model = Article
	form_class = ArticleForm
	template_name = "wiki_article_update.html"

	def get_success_url(self):
		return reverse_lazy('wiki:article-detail', kwargs={'pk': self.object.pk})
	
	def form_valid(self, form):
		form.instance.user=self.request.user
		return super().form_valid(form)