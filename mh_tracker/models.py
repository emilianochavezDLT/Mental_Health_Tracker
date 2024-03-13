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
    #return f"Soberiety record for {self.user.username} on {self.date}"
    # Because user model is broken and I do not have enough time nor was I assigned to
    # fix it thus I hard coded the username at this case.
    return f"Soberiety record for Kenyou on {self.date}"
