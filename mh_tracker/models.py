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
