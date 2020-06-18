from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text','image')

class SearchForm(forms.Form):
    query=forms.CharField()

    def clean_query(self):
        c_query=self.cleaned_data['query']
        return c_query

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('author', 'text')