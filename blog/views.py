from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Article, ArticleCategory
from .forms import ArticleForm, CommentForm
from user_management.models import Profile
from hobbysite import settings


class ArticleListView(ListView):
    model = ArticleCategory
    template_name = 'blog_article_listview.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            author = Profile.objects.get(user=self.request.user)
            ctx['articlesByAuthor'] = Article.objects.filter(author=author)
        return ctx


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog_article_detailview.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        article = self.get_object()
        author = article.author
        ctx['articlesByAuthor'] = Article.objects.filter(author=author)
        if self.request.user.is_authenticated:
             author = article.author
             ctx['articlesByAuthor'] = Article.objects.filter(author=author)
             ctx['user'] = author
             ctx['form'] = CommentForm(initial={'user': author, 'article': article})
        return ctx

    def post(self, request, **kwargs):
        form = CommentForm(request.POST)
        article = self.get_object()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = Profile.objects.get(user=self.request.user)
            comment.article = article
            comment.save()
            return redirect('blog:article-detail', pk=article.pk)
        ctx = self.get_context_data(**kwargs)
        return self.render_to_response(ctx)


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "blog_article_createview.html"
    
    def get_success_url(self):
	    return reverse_lazy('blog:article-detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        form.instance.user = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        author = Profile.objects.get(user=self.request.user)
        ctx['form'] = ArticleForm(initial={'author': author})
        return ctx
    
    def get_initial(self):
        author = Profile.objects.get(user=self.request.user)
        return {'author':author}


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "blog_article_updateview.html"

    def get_success_url(self):
	    return reverse_lazy('blog:article-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)