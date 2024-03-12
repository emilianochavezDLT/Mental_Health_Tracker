from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  extra_journal = models.BooleanField("Afternoon Journal?", default=False)

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



