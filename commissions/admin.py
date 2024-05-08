from django.contrib import admin
from .models import Job, Commission, JobApplication

class CommentInline(admin.StackedInline):
    model = Job

class CommissionAdmin(admin.ModelAdmin):
    model = Commission
    inlines = [CommentInline,]
    
class JobApplicationAdmin(admin.ModelAdmin):
    model = JobApplication
    
    
admin.site.register(Commission, CommissionAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)

