from django.db import models
from django.urls import reverse
from user_management.models import Profile

# Create your models here.
class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']       

class Article(models.Model):
    title = models.CharField(max_length=255)
    article_author = models.ForeignKey(
        Profile,
        on_delete = models.SET_NULL,
        null = True,
        related_name = 'article_author'
    )
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    header_image = models.ImageField(upload_to='images/', null=True, blank=True)
    article_category = models.ForeignKey(
        ArticleCategory, 
        on_delete = models.SET_NULL,
        null = True,
        related_name = 'article_category'
    )
    
    
    class Meta:
        ordering = ['-created_on']
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('wiki:article-detail', args=[self.pk])
    
class Comment(models.Model):
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    comment_author = models.ForeignKey(
        Profile,
        on_delete = models.SET_NULL,
        null = True,
        related_name = 'comment_author_wiki'
    )

    comment_article = models.ForeignKey(
        Article,
        on_delete = models.CASCADE,
        related_name = 'comment_article'
    )


    class Meta:
        ordering = ['created_on']
