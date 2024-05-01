import calendar
import datetime as datetime
import json

import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

#from django_project.settings import EMAIL_HOST_PASSWORD_1, EMAIL_HOST_USER_1
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.timezone import now

from mh_tracker.models import Article, JournalEntry, Therapist, Videos

from .forms import LoginForm, SignupForm, TherapistForm
from .models import SubstanceAbuseTracking, User
from .tasks import send_email_report_task


# Create your views here.
def home(request):
  #check if user has already done their journal entry
  userNow = User.objects.filter(username=request.user)
  entryCmplt = 'false'
  if request.user.is_authenticated:
    d = datetime.date.today()
    data = JournalEntry.objects.filter(user=userNow[0].id).last()
    if data is not None:
      entryCmplt = data.entry_complete(d)
  #carousel api
  quotes = []
  for i in range(5):
    r = requests.get('https://zenquotes.io/api/random')
    quotes.append(r.json()[0]['h'])
  return render(request, 'mh_tracker/home.html', {
      'quotes': quotes,
      'entryDoneToday': entryCmplt
  })


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
  if request.user.is_authenticated:
    return redirect('settings')
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


@login_required
def color_calendar(request):
  if request.method == 'POST':
    #Redirect to the homepage
    return redirect('mh_tracker/home.html')
  else:
    #Render the form
    return render(request, 'mh_tracker/color_calendar.html')


@login_required
def settings(request):
  if request.method == 'POST':
    #Redirect to the homepage
    return redirect('mh_tracker/home')
  else:
    #Render the form
    #We need to send therapists to the settings page
    therapists = Therapist.objects.all()
    if therapists.exists():
      print(therapists)
      therapist_list = [{
          'first_name': therapist.first_name,
          'last_name': therapist.last_name,
          'email': therapist.email,
          'company': therapist.company,
          'phone_number': therapist.phone_number
      } for therapist in therapists]
    else:
      therapist_list = None

    context = {
        'therapist_list': therapist_list,
    }
    return render(request, 'mh_tracker/settings.html', context)


@login_required
def analytics(request):
  if request.method == 'POST':
    #Redirect to the homepage
    return redirect('mh_tracker/home.html')
  else:
    #Render the form
    return render(request, 'mh_tracker/analytics.html')


@login_required
def substance_abuse_chart(request, year=None, month=None):
  user = request.user
  if year is None or month is None:
    now = datetime.date.today()
  else:
    now = datetime.date(year=int(year), month=int(month), day=1)

  start_date = now.replace(day=1)
  end_date = now.replace(day=calendar.monthrange(now.year, now.month)[1])
  substance_data = SubstanceAbuseTracking.objects.filter(
      user=user, date__range=(start_date, end_date)).order_by('date')

  date_counter_map = {
      entry.date.strftime('%Y-%m-%d'): entry.counter
      for entry in substance_data
  }

  dates = [
      start_date + datetime.timedelta(days=x)
      for x in range((end_date - start_date).days + 1)
  ]
  dates_formatted = [date.strftime('%Y-%m-%d') for date in dates]
  counters = [date_counter_map.get(date, 0) for date in dates_formatted]

  context = {
      'dates': dates_formatted,
      'counters': counters,
      'current_year': now.year,
      'current_month': now.month,
  }

  return render(request, 'mh_tracker/substance_abuse_chart.html', context)


def current_month_date_range():
  now = datetime.date.today()
  start_date = now.replace(day=1)
  end_date = now.replace(day=calendar.monthrange(now.year, now.month)[1])
  return start_date, end_date


@login_required
def update_substance_use(request, action):
  if request.method == 'POST':
    today = now().date()
    entry, created = SubstanceAbuseTracking.objects.get_or_create(
        user=request.user, date=today, defaults={'counter': 0})
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


def calendar_data(request):
  journal_entries = JournalEntry.objects.filter(
      user=request.user).order_by('date_created')
  events = []
  for entry in journal_entries:
    events.append({
        'title': 'Sleep: {}'.format(entry.sleep_quality),
        'start': entry.date_created.strftime('%Y-%m-%d'),
        'end': entry.date_created.strftime('%Y-%m-%d'),
        'color': '#FFA07A'
    })
    events.append({
        'title': 'Exercise: {}'.format(entry.exercise_time),
        'start': entry.date_created.strftime('%Y-%m-%d'),
        'end': entry.date_created.strftime('%Y-%m-%d'),
        'color': '#90EE90'
    })
    events.append({
        'title': 'Diet: {}'.format(entry.diet_quality),
        'start': entry.date_created.strftime('%Y-%m-%d'),
        'end': entry.date_created.strftime('%Y-%m-%d'),
        'color': '#87CEEB'
    })
    events.append({
        'title': 'Water: {}'.format(entry.water_intake),
        'start': entry.date_created.strftime('%Y-%m-%d'),
        'end': entry.date_created.strftime('%Y-%m-%d'),
        'color': '#ADD8E6'
    })
    events.append({
        'start': entry.date_created.strftime('%Y-%m-%d'),
        'end': entry.date_created.strftime('%Y-%m-%d'),
        'color': get_mood_color(entry.mood_level),
        'display': 'background'
    })

  return JsonResponse(data=events, safe=False)


def get_mood_color(mood_level):
  color_mapping = {
      1: '#FF0000',  # Red
      2: '#FFA500',  # Orange
      3: '#FFFF00',  # Yellow
      4: '#32CD32',  # Lime Green
      5: '#00FF00',  # Green
  }
  return color_mapping.get(mood_level, '#FFFFFF')


def rescourcesPage(request):
  videos = Videos.objects.all()
  articles = Article.objects.all()
  context = {'videos': videos, 'articles': articles}
  return render(request, 'mh_tracker/resources.html', context)


@login_required
def reports(request):
  if request.method == 'GET':
    #Dictionary for passing in context
    context = {}

    #Gets the Journal Entries for the user for the past 31 days
    d = datetime.date.today() - datetime.timedelta(days=31)
    data = JournalEntry.objects.filter(user=request.user, date_created__gte=d)

    #Input names used for the Report
    inputNamesNegative = {
        'mood_level__lte': 'mood_negative',
        'sleep_quality__lte': 'sleep_negative',
        'exercise_time__lte': 'exercise_negative',
        'diet_quality__lte': 'diet_negative',
        'water_intake__lte': 'water_negative'
    }
    inputNamesNeutral = {
        'mood_level__exact': 'mood_neutral',
        'sleep_quality__exact': 'sleep_neutral',
        'diet_quality__exact': 'diet_neutral'
    }
    inputNamesPositive = {
        'mood_level__gte': 'mood_positive',
        'sleep_quality__gte': 'sleep_positive',
        'exercise_time__gte': 'exercise_positive',
        'diet_quality__gte': 'diet_positive',
        'water_intake__gte': 'water_positive'
    }

    #Filters for the data used to generate the Report
    filtersLessThan = {
        'mood_level__lte': 2,
        'sleep_quality__lte': 2,
        'exercise_time__lte': 59,
        'diet_quality__lte': 2,
        'water_intake__lte': 7
    }
    filtersNeutral = {
        'mood_level__exact': 3,
        'sleep_quality__exact': 3,
        'diet_quality__exact': 3,
    }
    filtersGreaterThan = {
        'mood_level__gte': 4,
        'sleep_quality__gte': 4,
        'exercise_time__gte': 60,
        'diet_quality__gte': 4,
        'water_intake__gte': 8
    }

    #Generates the data for the Report
    helper_reports_general(filtersLessThan, inputNamesNegative, data, context)
    helper_reports_general(filtersNeutral, inputNamesNeutral, data, context)
    helper_reports_general(filtersGreaterThan, inputNamesPositive, data,
                           context)

    #Gathers the journal entry data and adds it to the context dictionary
    temp_data = data.filter(journal_text="")
    context.update({"journal_entries_negative": temp_data.count()})
    temp_data = data.filter(~Q(journal_text=""))
    context.update({"journal_entries_positive": temp_data.count()})

    #Adds to auto check for Therapist checkbutton
    #check_Bool = false
    #if request.user.therapist_check:
    #check_Bool = true
    #context.update({"therapist_check" : check_Bool})

    return render(request, 'mh_tracker/reports.html', context)
  else:
    return redirect('mh_tracker/home.html')


def helper_reports_general(filters, inputNames, data, context):
  #For each set in the filters dictionary
  for key, value in filters.items():
    #Filter the data based on the key and value and add these to the context
    temp_data = data.filter(**{key: value})
    context.update({inputNames[key]: temp_data.count()})
    #If the mood was filtered, then calculate the averages based on the mood
    if 'mood' in key:
      if 'lte' in key:
        helper_reports_average(temp_data, context, '_negative')
      else:
        helper_reports_average(temp_data, context, '_positive')


def helper_reports_average(data, context, type):

  #Names of each Avg and Stats is the total of each statistic
  inputNamesAvg = [
      'sleepAvg', 'exerciseAvg', 'dietAvg', 'waterAvg', 'journalAvg'
  ]
  stats = [0, 0, 0, 0, 0]

  #Gathers the data necessary for stats by adding up the sum of each value
  for item in data:
    stats[0] += item.sleep_quality
    stats[1] += item.exercise_time
    stats[2] += item.diet_quality
    stats[3] += item.water_intake
    if item.journal_text != "":
      stats[4] += 1

  #For each stat, if the count of the stat is equla to 0, then set every value to 0 or not
  #If the value is 4, then update it's doing a journal entry and set it to nothing or not
  #Lastly, if it's a regular value then calculate the average of it
  for i in range(0, len(stats)):
    if data.count() == 0:
      if i != 4:
        context.update({inputNamesAvg[i] + type: 0})
      else:
        context.update({inputNamesAvg[i] + type: 'not'})
    elif i == 4:
      temp = '' if stats[4] >= 0.5 else 'not'
      context.update({inputNamesAvg[i] + type: temp})
    else:
      stats[i] /= data.count()
      stats[i] = round(stats[i], 2)
      context.update({inputNamesAvg[i] + type: stats[i]})


def send_email_report(request):
  data = json.loads(request.body)
  Subject = data.get('Subject')
  Message = data.get('Message')
  Message = Message.replace(
      'you', request.user.first_name + ' ' + request.user.last_name)
  Emails = [request.user.email]
  user_therapist = Therapist.objects.filter(user=request.user).last()
  #Sends an email to the user with the request information
  if data.get('Therapist') and user_therapist is not None:
    Emails.append(user_therapist.email)
  result = send_email_report_task(Subject, Message, Emails)
  return JsonResponse({'result': result})


# Add a therapist for the user to have
def add_therapist(request):
  if request.method == 'POST':
    therapist_form = TherapistForm(request.POST)
    if therapist_form.is_valid():
      therapist = therapist_form.save(commit=False)
      #Assigning the logged in user to the therapist
      therapist.user = request.user
      therapist.save()
      return redirect('home')
  else:
    therapist = TherapistForm()
    return render(request, 'mh_tracker/add_therapist.html',
                  {'therapist': therapist})


# View all therapists
#I might have to put all of this into the settings view!!
def view_therapists(request):
  therapists = Therapist.objects.all()
  if therapists:
    return render(request, 'mh_tracker/settings.html', {'therapists': None})
  else:
    return render(request, 'mh_tracker/settings.html',
                  {'therapists': therapists})
