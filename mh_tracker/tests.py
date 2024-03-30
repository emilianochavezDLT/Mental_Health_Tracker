from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import JournalEntry, SubstanceAbuseTracking, Article, Videos
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

  def test_journal_entry_creation(self):
    self.assertEqual(self.journal_entry.mood_level, 5)

  def test_substance_abuse_tracking_creation(self):
    self.assertEqual(self.substance_abuse_tracking.days_sober, 10)

  def test_article_creation(self):
    self.assertEqual(self.article.title, "Test Article")

  def test_video_creation(self):
    self.assertEqual(self.video.description, "A test video.")


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