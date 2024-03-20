from django.db import models
from datetime import datetime
from django.urls import reverse

class Commission(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    people_required = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('commissions:commission_detail', args=[str(self.pk)])


    class Meta:
        ordering = ['updated_on']

class Comment(models.Model):
    commission = models.ForeignKey(
        Commission,
        related_name="comment",
        on_delete=models.CASCADE
    )

    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.entry
    
    
    class Meta:
        ordering = ['created_on']


    