from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class SignUpForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=6,  # forces at least 6 chars
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already taken!")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already in use!")
        return email
