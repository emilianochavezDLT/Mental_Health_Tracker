from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import SubstanceAbuseTracking


class SignupForm(UserCreationForm):

  class Meta:
    model = User
    fields = [
        'first_name', 'last_name', 'username', 'email', 'password1',
        'password2'
    ]


class LoginForm(forms.Form):
  username = forms.CharField()
  password = forms.CharField(widget=forms.PasswordInput)


