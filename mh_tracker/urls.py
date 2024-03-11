from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('journal-entry/', views.journal_entry, name='journal_entry'), 
    path('color_calendar/', views.color_calendar, name='color_calendar'),
    path('settings/', views.settings, name='settings'), 
    path('login/', views.user_login, name='login'), 
    path('signup/', views.user_signup, name='signup'), 
    path('analytics/', views.analytics, name='analytics'), 
  
  
]
