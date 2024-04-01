from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import SubstanceAbuseTracking
from .tasks import send_feedback_email_task


class SignupForm(UserCreationForm):

  class Meta:
    model = User
    fields = [
        'first_name', 'last_name', 'username', 'email', 'password1',
        'password2'
    ]

  def send_email(self):
    send_feedback_email_task.delay(
        self.cleaned_data['email'],
        self.cleaned_data['username'])  # type: ignore


class LoginForm(forms.Form):
  username = forms.CharField()
  password = forms.CharField(widget=forms.PasswordInput)
