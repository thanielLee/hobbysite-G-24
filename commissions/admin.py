from django.contrib import admin
from .models import Job, Commission, JobApplication

class CommentInline(admin.StackedInline):
    model = Job

class CommissionAdmin(admin.ModelAdmin):
    model = Commission
    inlines = [CommentInline,]
    
admin.site.register(Commission, CommissionAdmin)

