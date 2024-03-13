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
  video_link = models.URLField(blank=True, null=True) #For youtube videos
  video_file = models.FileField(upload_to='resources/', blank=True, null=True)

  #These are two helper methods to determine if a video is a link or file
  def is_video_link(self):
    return bool(self.video_link)

  def is_uploaded_video(self):
    return bool(self.video_file)

  def __str__(self):
    return f"Soberiety record for {self.user.username} on {self.date}"

'''
#User Journal settings
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  dbl_journal = models.BooleanField(default=False)
  track_sleep_quality = models.BooleanField("Track Sleep", default=False)
  track_exercise_time = models.BooleanField("Track Exercise", default=False)
  track_diet_quality = models.BooleanField("Track Diet", default=False)
  track_water_intake = models.BooleanField("Track Water Intake", default=False)
  track_thoughts = models.BooleanField("Track Thoughts", default=False)
'''
