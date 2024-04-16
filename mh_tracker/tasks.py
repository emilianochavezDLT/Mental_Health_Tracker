from time import sleep
from django.core.mail import send_mail
from celery import shared_task
from mh_tracker.models import User


@shared_task()
def send_register_email_task(email_address, username):
    """Sends an email when the signup form has been submitted."""
    sleep(20)  # Simulate expensive operation(s) that freeze Django
    send_mail(
      'Welcome to Spectrum Diary: Mental Health Tracker', #subject
      f'Hi {username}! We are glad to see you taking steps to '+ 
      'improve your mental health.', #message
      "jbraitsc@uccs.edu", #sender email
      [email_address], #recipient email
      fail_silently=False,
  )


@shared_task(name="send_reminder_email_task")
def send_reminder_email_task():
    users=User.objects.first()
    print(users)
    for user in users:
      sleep(20)
      send_mail(
      'Welcome to Spectrum Diary: Mental Health Tracker', #subject
      f'Hi {user.username}! We hope you had a productive day today and '+ 
      'we cannot wait to hear all about it! This is your reminder '+
      'to fill out your daily journal to keep track of your health.', #message
      "jbraitsc@uccs.edu", #sender email
      [user.email_address], #recipient email
      fail_silently=False,
    )