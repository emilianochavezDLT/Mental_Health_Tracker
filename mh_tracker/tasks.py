from time import sleep
from django.core.mail import send_mail
from celery import shared_task
from mh_tracker.models import User
from celery import Celery

# Emails new user after registration
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


# Emails user daily to fill out their daily journal entry
@shared_task(name="send_reminder_email_task")
def send_reminder_email_task():
    users=User.objects.exclude(username='admin')
    for user in users:
      send_mail(
      'Journal Entry Reminder', #subject
      f'Hi {user.username}! We hope you had a productive day today and '+ 
      'we cannot wait to hear all about it! This is your reminder '+
      'to fill out your daily journal to keep track of your health.', #message
      "jbraitsc@uccs.edu", #sender email
      [user.email], #recipient email
      fail_silently=False,
      )

# Test to verify that Periodic Tasks are working
@shared_task(name="checker")
def check():
  print("I am checking your stuff")

# Emails a user's report
@shared_task()
def send_email_report_task(subject, message, emails):
  #Sends report
  sleep(20)  # Simulate expensive operation(s) that freeze Django
  result = send_mail(
      subject,  #subject
      message,  #message
      "jbraitsc@uccs.edu",  #sender email
      emails,  #recipient email
      fail_silently=False,
  )
  return result
