from django.contrib import admin
from .models import *

#Register models
admin.site.register(JournalEntry)
admin.site.register(SubstanceAbuseTracking)
admin.site.register(Article)
admin.site.register(Videos)
admin.site.register(Therapist)
