from django.db import models
from django.urls import reverse

# Create your models here.
class PostCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('forum:thread-list', args=[str(self.pk)])

    class Meta:
        ordering = ['name']


class Post(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        "PostCategory",
        on_delete = models.SET_NULL,
        related_name = "posts",
        null = True,
    )
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('forum:thread-detail', args=[str(self.pk)])
    
    class Meta:
        ordering = ['-created_on']