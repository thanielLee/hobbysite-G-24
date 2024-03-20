from django.db import models
from django.urls import reverse

# Create your models here.
class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']       

class Article(models.Model):
    title = models.CharField(max_length=255)
    entry = models.TextField(default='ArticleEntry')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    article_category = models.ForeignKey(
        ArticleCategory, 
        on_delete=models.SET_NULL,
        null = True,
        related_name='article')
    
    
    class Meta:
        ordering = ['-created_on']
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('wiki:article-detail', args=[self.pk])