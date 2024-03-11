from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import JournalEntry
from .forms import JournalEntryForm

# Create your views here.
def home(request):
  return render(request, 'mh_tracker/home.html')


#User can long in their journal entry
@login_required
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
def user_login(request):
  if request.method == 'POST':
      username = request.POST['username']
      password = request.POST['password']
      user = authenticate(request, username=username, password=password)
      if user is not None:
          login(request, user)
          return redirect('journal_entry')
      else:
          # Handle invalid login
          return render(request, 'mh_tracker/login.html', {'error': 'Invalid credentials'})
  return render(request, 'mh_tracker/login.html')

def user_logout(request):
  logout(request)
  return redirect('login')
  
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
