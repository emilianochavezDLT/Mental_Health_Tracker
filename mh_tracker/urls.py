from django.contrib import admin
from django.urls import path
from . import views
from .views import update_substance_use

urlpatterns = [
    path('', views.home, name='home'),
    path('journal-entry/', views.journal_entry, name='journal_entry'),
    path('color_calendar/', views.color_calendar, name='color_calendar'),
    path('settings/', views.settings, name='settings'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.user_signup, name='signup'),
    path('analytics/', views.analytics, name='analytics'),
    path('substance_abuse_chart/',
         views.substance_abuse_chart,
         name='substance_abuse_chart'),
    path('substance_use/increment/',
         lambda request: update_substance_use(request, 'increment'),
         name='increment_substance_use'),
    path('substance_use/reset/',
         lambda request: update_substance_use(request, 'reset'),
         name='reset_substance_use'),
    #path('user/<int:pk>progression', views.UserView.as_view(), name="user_detail"),
    path('user/progression', views.user_progression, name="user_progression"),
    path('calendar/data', views.calendar_data, name="calendar_data"),
    path('get_journal_entries/',
         views.get_journal_entries,
         name='get_journal_entries'),
    path('resources/', views.rescourcesPage, name='resources'),
    path('reports/', views.reports, name='reports'),
    path('add_therapist/', views.add_therapist, name='add_therapist'),
    path('send_email_report/', views.send_email_report, name='send_email_report'),
]
