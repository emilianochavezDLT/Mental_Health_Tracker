from django.shortcuts import render, redirect


# Create your views here.
def home(request):
  return render(request, 'mh_tracker/home.html')

#User can long in their journal entry
def journal_entry(request):
  if request.method == 'POST':
    #Redirect to the homepage
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