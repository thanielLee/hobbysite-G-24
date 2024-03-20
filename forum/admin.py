from django.contrib import admin

from .models import Post, PostCategory
# Register your models here.

class PostInline(admin.TabularInline):
    model = Post

class PostCategoryAdmin(admin.ModelAdmin):
    model = PostCategory
    inlines = [PostInline,]

class PostAdmin(admin.ModelAdmin):
    model = Post


admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)