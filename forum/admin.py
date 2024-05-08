from django.contrib import admin

from .models import Thread, ThreadCategory, Comment
# Register your models here.

class ThreadInline(admin.TabularInline):
    model = Thread

class ThreadCategoryAdmin(admin.ModelAdmin):
    model = ThreadCategory
    inlines = [ThreadInline,]

class ThreadAdmin(admin.ModelAdmin):
    model = Thread

class CommentInline(admin.TabularInline):
    model = Comment

admin.site.register(Thread, ThreadAdmin)
admin.site.register(ThreadCategory, ThreadCategoryAdmin)