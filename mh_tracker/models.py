from django.db import models
from django.contrib.auth.models import User

# Create your models here.


#Captures information from user
class JournalEntry(models.Model):
  user = models.ForeignKey(User,
                           on_delete=models.CASCADE)  #Links to a specfic user
  date_created = models.DateTimeField(
      auto_now_add=True)  #Date and time of entry
  mood_level = models.IntegerField()  # 1 to 5
  sleep_quality = models.IntegerField()  #1 to 5
  exercise_time = models.IntegerField()  # in minutes
  diet_quality = models.IntegerField()  #1 to 5
  water_intake = models.IntegerField()  #1 to 5
  journal_text = models.TextField()  #Keep track of journal entry texts

  #Return time created by user
  def __str__(self):
    return f"Journal Entry by {self.user.username} on {self.date_created.strftime('%m/%d/%Y')}"
