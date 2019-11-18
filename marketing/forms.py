from django import forms
from .models import Signup, AccessTutorialSignup


class EmailSignupForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        "type": "email",
        "name": "email",
        "id": "email",
        "placeholder": "Type your email address",
    }), label="")

    class Meta:
        model = Signup
        fields = ('email', )


class AccessTutorialSignupForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        "type": "email",
        "name": "email",
        "id": "email",
        "placeholder": "Type your email address",
    }), required=True, label="")
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Type your first name",
    }), required=True, label="")
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Type your last name",
    }), required=True, label="")
    hobby = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "What's your favorite hobby?",
    }), required=True, label="")

    class Meta:
        model = AccessTutorialSignup
        fields = ('email', 'first_name', 'last_name', 'hobby', )