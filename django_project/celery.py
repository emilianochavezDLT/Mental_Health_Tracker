import os
from celery import Celery
from celery.schedules import crontab

#Defining a Celery Instance
#From developer documentation

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

app = Celery('django_project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    # Executes everyday at 6:30 p.m.
    'send_email_reminder': {
        'task': 'send_reminder_email_task',
        'schedule': crontab(minute='24', hour='2', day_of_week='0-6'),
    },
  #just for testing beat works
   'run-me-every-thirty-seconds': {
   'task': 'checker',
   'schedule': 30.0,
    },
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()