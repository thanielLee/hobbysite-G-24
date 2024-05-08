from django.contrib import admin
from .models import Article, ArticleCategory, Comment


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    model = Article
   
class ArticleCategoryAdmin(admin.ModelAdmin):    
    model = ArticleCategory
    
class CommentInLine(admin.StackedInline):
    model = Comment
    
class CommentAdmin(admin.ModelAdmin):
    model = Comment

admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Comment, CommentAdmin)