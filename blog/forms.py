from django import forms
from .models import ArticleCategory, Article, Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        #fields = ['title','category','entry','headerImage',]
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].disabled = True


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['entry']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



