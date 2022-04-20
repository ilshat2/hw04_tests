from django import forms
from posts.models import Post


class PostForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = Post
        fields = ('text', 'group')
