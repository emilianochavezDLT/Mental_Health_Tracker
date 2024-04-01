from django.db import models
from django.contrib.auth.models import User


class JournalEntry(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  date_created = models.DateTimeField(auto_now_add=True)
  mood_level = models.IntegerField()
  sleep_quality = models.IntegerField()
  exercise_time = models.IntegerField()
  diet_quality = models.IntegerField()
  water_intake = models.IntegerField()
  journal_text = models.TextField()

  def __str__(self):
    return f"Journal Entry by {self.user.username} on {self.date_created.strftime('%m/%d/%Y')}"


class SubstanceAbuseTracking(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  date = models.DateField(auto_now_add=True)
  days_sober = models.IntegerField(default=0)
  counter = models.IntegerField(default=0)


'''
The articles models and videos models are part the of the
resources portion of the application.

The article takes in a pdf file,title, and description.

The video model takes in a video file, title, and description.
'''


class Article(models.Model):
  title = models.CharField(max_length=100)
  description = models.TextField()
  pdf = models.FileField(upload_to='resources/')


class Videos(models.Model):
  title = models.CharField(max_length=100)
  description = models.TextField()
  video_link = models.URLField(blank=True, null=True)  #For youtube videos
  video_file = models.FileField(upload_to='resources/', blank=True, null=True)

  #These are two helper methods to determine if a video is a link or file
  def is_video_link(self):
    return bool(self.video_link)

  def is_uploaded_video(self):
    return bool(self.video_file)

  def __str__(self):
    return f"Soberiety record for {self.user.username} on {self.date}"


'''
Creating a model for therapists, so that the user can have a therapist.
The therapist model will have a one to one relationship with the user model.
'''

class Therapist(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  email = models.EmailField()
  company = models.CharField(max_length=50)
  phone_number = models.CharField(max_length=15)

  def __str__(self):
    return f"Therapist for {self.user.username}"



