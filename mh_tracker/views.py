from django.shortcuts import render, redirect
from mh_tracker.models import JournalEntry, User


# Create your views here.
def home(request):
  return render(request, 'mh_tracker/home.html')


#User can long in their journal entry
def journal_entry(request):
  #user = User.objects.get(pk=pk)
  if request.method == 'POST':
    #Redirect to the homepage
    journal_Entry = JournalEntry(
        user_id=1,
        #user_id=request.user.id,
        mood_level=request.POST['mood_level'],
        sleep_quality=request.POST['sleep_quality'],
        exercise_time=request.POST['exercise_time'],
        diet_quality=request.POST['diet_quality'],
        water_intake=request.POST['water_intake'],
        journal_text=request.POST['journal_text'])
    JournalEntry.save(journal_Entry)
    return redirect('home')
  else:
    #Render the form
    return render(request, 'mh_tracker/journal_entry.html')


def color_calendar(request):
  if request.method == 'POST':
    #Redirect to the homepage
    return redirect('home')
  else:
    #Render the form
    return render(request, 'mh_tracker/color_calender.html')


def settings(request):
  if request.method == 'POST':
    #Redirect to the homepage
    return redirect('home')
  else:
    #Render the form
    return render(request, 'mh_tracker/settings.html')


def login(request):
  if request.method == 'POST':
    #Redirect to the homepage
    return redirect('home')
  else:
    #Render the form
    return render(request, 'mh_tracker/login.html')


def signup(request):
  if request.method == 'POST':
    #Redirect to the homepage
    return redirect('home')
  else:
    #Render the form
    return render(request, 'mh_tracker/signup.html')


def analytics(request):
  if request.method == 'POST':
    #Redirect to the homepage
    return redirect('home')
  else:
    #Render the form
    return render(request, 'mh_tracker/analytics.html')
