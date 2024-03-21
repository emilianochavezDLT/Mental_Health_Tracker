from time import sleep
from django.core.mail import send_mail
from celery import shared_task

@shared_task()
def send_feedback_email_task(email_address, username):
    """Sends an email when the feedback form has been submitted."""
    sleep(20)  # Simulate expensive operation(s) that freeze Django
    send_mail(
      'Welcome to Spectrum Diary: Mental Health Tracker', #subject
      f'Hi {username}! We are glad to see you taking steps to '+ 
      'improve your mental health.', #message
      "support@example.com", #sender email
      [email_address], #recipient email
      fail_silently=False,
    )