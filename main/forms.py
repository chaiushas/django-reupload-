from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', 'product', 'commenter',)
        widgets = {'book': forms.HiddenInput(), 'reviewer': forms.HiddenInput()}