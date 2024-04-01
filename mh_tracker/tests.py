from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import JournalEntry, SubstanceAbuseTracking, Article, Videos, Therapist
from datetime import datetime


class ModelsTestCase(TestCase):

  def setUp(self):

    self.user = User.objects.create_user(username='testuser', password='12345')

    self.journal_entry = JournalEntry.objects.create(
        user=self.user,
        date_created=datetime.now(),
        mood_level=5,
        sleep_quality=4,
        exercise_time=30,
        diet_quality=3,
        water_intake=7,
        journal_text="Test entry")

    self.substance_abuse_tracking = SubstanceAbuseTracking.objects.create(
        user=self.user, days_sober=10, counter=2)

    self.article = Article.objects.create(title="Test Article",
                                          description="A test article.",
                                          pdf="path/to/pdf")

    self.video = Videos.objects.create(title="Test Video",
                                       description="A test video.",
                                       video_link="https://example.com")
    
    self.therapist = Therapist.objects.create(user = self.user, first_name = "John", last_name = "Doe", email = "jd@mail.com",  company = "Therapy Inc.", phone_number = "123-456-7890",)


  def test_journal_entry_creation(self):
    self.assertEqual(self.journal_entry.mood_level, 5)

  def test_substance_abuse_tracking_creation(self):
    self.assertEqual(self.substance_abuse_tracking.days_sober, 10)

  def test_article_creation(self):
    self.assertEqual(self.article.title, "Test Article")

  def test_video_creation(self):
    self.assertEqual(self.video.description, "A test video.")

  def test_therapist_creation(self):
    self.assertEqual(self.therapist.first_name, "John")
    self.assertEqual(self.therapist.last_name, "Doe")
    self.assertEqual(self.therapist.email, "jd@mail.com")
    self.assertEqual(self.therapist.company, "Therapy Inc.")
    self.assertEqual(self.therapist.phone_number, "123-456-7890")
    self.assertEqual(self.therapist.user, self.user)


class URLAccessTestCase(TestCase):

  def setUp(self):

    self.client = Client()

    self.user = User.objects.create_user(username='testuser', password='12345')
    self.client.login(username='testuser', password='12345')

  def test_home_access(self):
    response = self.client.get(reverse('home'))
    self.assertEqual(response.status_code, 200)

  def test_login_access(self):
    self.client.logout()
    response = self.client.get(reverse('login'))
    self.assertEqual(response.status_code, 200)

  def test_protected_url_redirects(self):
    self.client.logout()
    response = self.client.get(reverse('journal_entry'))

    self.assertTrue(response.status_code, 302)

  def test_journal_entry_access(self):
    response = self.client.get(reverse('journal_entry'))
    self.assertEqual(response.status_code, 200)

  def test_reports_access(self):
    response = self.client.post(reverse('reports'))
    self.assertEqual(response.status_code, 200)


class JournalEntryTestCase(TestCase):

  def setUp(self):

    self.user = User.objects.create_user(username='testuser', password='12345')
    self.client.login(username='testuser', password='12345')

  def test_journal_entry(self):
    request = {
        'user': self.user,
        'date_created': datetime.today(),
        'mood_level': 5,
        'sleep_quality': 4,
        'exercise_time': 3,
        'diet_quality': 2,
        'water_intake': 1,
        'journal_text': 'Test entry'
    }

    self.client.post(reverse('journal_entry'), request)
    self.assertTrue(JournalEntry.objects.filter(user=self.user).exists())


class ReportsTestCase(TestCase):

  def setUp(self):

    self.user = User.objects.create_user(username='testuser', password='12345')
    self.client.login(username='testuser', password='12345')


def test_reports(self):
  request = {
      'user': self.user,
      'date_created': datetime.today(),
      'mood_level': 5,
      'sleep_quality': 4,
      'exercise_time': 3,
      'diet_quality': 2,
      'water_intake': 1,
      'journal_text': 'Test entry'
  }

  response = self.client.post(reverse('reports'), request)

  result = {
      "mood_negative": 1,
      "mood_neutral": 0,
      "mood_positive": 0,
      "sleep_negative": 1,
      "sleep_neutral": 0,
      "sleep_positive": 0,
      "exercise_negative": 0,
      "exercise_neutral": 1,
      "exercise_positive": 0,
      "diet_negative": 1,
      "diet_neutral": 0,
      "diet_positive": 0,
      "water_negative": 1,
      "water_neutral": 0,
      "water_positive": 0,
      "journal_entries_negative": 0,
      "journal_entries_positive": 1
  }

  self.assertEqual(response.context == result)
