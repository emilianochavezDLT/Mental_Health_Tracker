from django.shortcuts import render, redirect
from django.http import JsonResponse
from mh_tracker.models import JournalEntry, User, Article, Videos
from django.http import JsonResponse, HttpResponseRedirect
from mh_tracker.models import JournalEntry, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm
from .models import SubstanceAbuseTracking
from django.urls import reverse
from django.utils.timezone import now
from django.core.mail import send_mail
from django_project.settings import EMAIL_HOST_USER
import requests


# Create your views here.
def home(request):
  quotes = []
  for i in range(2):
    r = requests.get('https://zenquotes.io/api/random')
    quotes.append(r.json()[0]['h'])
  return render(request, 'mh_tracker/home.html', {'quotes': quotes})


# signup page
def user_signup(request):
  if request.method == 'POST':
    form = SignupForm(request.POST)
    if form.is_valid():
      form.send_email()
      form.save()
      return redirect('home')
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
        return redirect('home')
  else:
    form = LoginForm()
  return render(request, 'mh_tracker/login.html', {'form': form})


# logout page
def user_logout(request):
  logout(request)
  return redirect('home')


#User can long in their journal entry
@login_required
def journal_entry(request):
  if request.method == 'POST':
    journal_Entry = JournalEntry(user=request.user,
                                 mood_level=request.POST['mood_level'],
                                 sleep_quality=request.POST['sleep_quality'],
                                 exercise_time=request.POST['exercise_time'],
                                 diet_quality=request.POST['diet_quality'],
                                 water_intake=request.POST['water_intake'],
                                 journal_text=request.POST['journal_text'])
    journal_Entry.save()
    return redirect('home')
  else:
    return render(request, 'mh_tracker/journal_entry.html')


def get_journal_entries(request):
  # Define fake mood data for specific dates
  mood_data = {
      "2024-03-01": {
          "mood_level": 3
      },
      "2024-03-05": {
          "mood_level": 5
      },
      # Add more entries as needed
  }

  return JsonResponse(mood_data)


def color_calendar(request):
  if request.method == 'POST':
    #Redirect to the homepage
    return redirect('mh_tracker/home.html')
  else:
    #Render the form
    return render(request, 'mh_tracker/color_calendar.html')


def settings(request):
  if request.method == 'POST':
    #Redirect to the homepage
    return redirect('mh_tracker/home')
  else:
    #Render the form
    return render(request, 'mh_tracker/settings.html')


@login_required
def analytics(request):
  if request.method == 'POST':
    #Redirect to the homepage
    return redirect('mh_tracker/home.html')
  else:
    #Render the form
    return render(request, 'mh_tracker/analytics.html')


@login_required
def substance_abuse_chart(request):
  user = request.user
  substance_data = SubstanceAbuseTracking.objects.filter(
      user=user).order_by('date')

  dates = [entry.date.strftime('%Y-%m-%d') for entry in substance_data]
  counters = [entry.counter for entry in substance_data]

  context = {
      'substance_data': substance_data,
      'dates': dates,
      'counters': counters,
  }

  return render(request, 'mh_tracker/substance_abuse_chart.html', context)


@login_required
def update_substance_use(request, action):
  if request.method == 'POST':
    today = now().date()
    entry, created = SubstanceAbuseTracking.objects.get_or_create(
        user=request.user,
        date=today,
        defaults={
            'days_sober': 0,
            'counter': 0
        }  # defaults are used if a new entry is created
    )
    if action == 'increment':
      entry.counter += 1
      entry.save()
    elif action == 'reset':
      entry.counter = 0
      entry.save()
    return HttpResponseRedirect(reverse('substance_abuse_chart'))
  else:
    return HttpResponseRedirect(reverse('home'))


@login_required
# View user progression
def user_progression(request):
  '''
    Gathers journal entry ratings and dates to display progression
    Convert data into JSON for Chart.js visulization 

    '''

  journal_entries = JournalEntry.objects.filter(
      user=request.user).order_by('date_created')
  dates = [
      entry.date_created.strftime('%Y-%m-%d') for entry in journal_entries
  ]
  moods = [entry.mood_level for entry in journal_entries]
  sleep = [entry.sleep_quality for entry in journal_entries]
  excercise = [entry.exercise_time for entry in journal_entries]
  diet = [entry.diet_quality for entry in journal_entries]
  water = [entry.water_intake for entry in journal_entries]
  context = {
      'dates': dates,
      'moods': moods,
      'sleep': sleep,
      'excercise': excercise,
      'diet': diet,
      'water': water,
  }
  return JsonResponse(data=context)


'''
def userPage(request, user_id):
  app_user = User.objects.get(id=user_id)
  profile = Profile.objects.get(user=app_user)
  form = UserForm()
  if request.method == 'POST':
    user_data = request.POST.copy()
    form = UserForm(user_data)
    if form.is_valid():
      appuser = form.save(commit=False)
      appuser.user = app_user
      return redirect('user_detail')
  context = {'form': form, 'app_user': app_user, 'profile': profile}
  return render(request, 'mh_tracker/user_form.html', context)
'''


def rescourcesPage(request):
  videos = Videos.objects.all()
  articles = Article.objects.all()
  context = {'videos': videos, 'articles': articles}
  return render(request, 'mh_tracker/resources.html', context)
