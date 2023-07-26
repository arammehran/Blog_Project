from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'name',
            'email',
            'role',
            "password1",
            "password2",

        ]
