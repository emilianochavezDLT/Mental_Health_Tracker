from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('journal-entry/', views.journal_entry, name='journal_entry'), #User can enter journal entry
   path('color_calendar/', views.color_calendar, name='color_calendar'), #Calendar URL
]
