from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)

class SearchForm(forms.Form):
    query=forms.CharField()

    def clean_query(self):
        c_query=self.cleaned_data['query']
        return c_query