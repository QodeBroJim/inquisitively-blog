from allauth.account.forms import SignupForm
from django import forms
from django.contrib import admin

from .models import Post, Comment
from ckeditor.fields import RichTextFormField


class PostForm(forms.ModelForm):
    content = RichTextFormField()

    class Meta():
        model = Post
        fields = ('title', 'slug', 'overview', 'content', 'thumbnail',
                'categories', 'featured', 'previous_post',
                'next_post')


class CommentForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your comment here',
        'id': 'usercomment',
        'rows': '4'
    }))

    class Meta:
        model = Comment
        fields = ('content', )

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30,
                                 label='First Name',
                                 widget=forms.TextInput(
                                     attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30,
                                label='Last Name',
                                widget=forms.TextInput(
                                    attrs={'placeholder': 'Last Name'}))

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user