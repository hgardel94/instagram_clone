from . models import Post, Comment
from django import forms

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('quote', 'image',)
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)