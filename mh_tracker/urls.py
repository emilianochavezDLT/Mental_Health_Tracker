from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('journal-entry/', views.journal_entry, name='journal_entry'),
    path('color_calendar/', views.color_calendar, name='color_calendar'),
    path('settings/', views.settings, name='settings'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.user_signup, name='signup'),
    path('analytics/', views.analytics, name='analytics'),
    #path('user/<int:pk>progression', views.UserView.as_view(), name="user_detail"),
    path('user/progression', views.user_progression, name="user_progression"),
    path('get_journal_entries/',
         views.get_journal_entries,
         name='get_journal_entries'),
]
