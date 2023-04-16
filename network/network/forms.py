import django.forms as forms
from .models import User, Post


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 10, 'placeholder': 'What is on your mind?'}), label='')

    class Meta:
        model = Post
        fields = ['user', 'content']
        widgets = {
            'user': forms.HiddenInput,
        }
