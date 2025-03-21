from django import forms
from .models import Post, Comment, Tag
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Extending the default UserCreationForm to add an email field
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class PostForm(forms.ModelForm):
    tags = forms.CharField(max_length=100, required=False, help_text="Add tags separated by commas")

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']

    def clean_tags(self):
        tag_names = self.cleaned_data['tags'].split(',')
        tags = []
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name.strip())
            tags.append(tag)
        return tags    

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your comment...'})      