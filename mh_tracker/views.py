from django.shortcuts import render, redirect
from mh_tracker.models import JournalEntry, User
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm



# Create your views here.
def home(request):
  return render(request, 'mh_tracker/home.html')


# signup page
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mh_tracker/login.html')
    else:
        form = SignupForm()
    return render(request, 'mh_tracker/signup.html', {'form': form})

# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('mh_tracker/home.html')
    else:
        form = LoginForm()
    return render(request, 'mh_tracker/login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('mh_tracker/login.html')
  
#User can long in their journal entry

def journal_entry(request):
        if request.method == 'POST':
            journal_Entry = JournalEntry(
                user=request.user,
                mood_level=request.POST['mood_level'],
                sleep_quality=request.POST['sleep_quality'],
                exercise_time=request.POST['exercise_time'],
                diet_quality=request.POST['diet_quality'],
                water_intake=request.POST['water_intake'],
                journal_text=request.POST['journal_text']
            )
            journal_Entry.save()
            return redirect('mh_tracker/home.html')
        else:
            return render(request, 'mh_tracker/journal_entry.html')


def color_calendar(request):
  if request.method == 'POST':
    #Redirect to the homepage
    return redirect('mh_tracker/home.html')
  else:
    #Render the form
    return render(request, 'mh_tracker/color_calender.html')


def settings(request):
  if request.method == 'POST':
    #Redirect to the homepage
    return redirect('mh_tracker/home')
  else:
    #Render the form
    return render(request, 'mh_tracker/settings.html')


def analytics(request):
  if request.method == 'POST':
    #Redirect to the homepage
    return redirect('mh_tracker/home.html')
  else:
    #Render the form
    return render(request, 'mh_tracker/analytics.html')
