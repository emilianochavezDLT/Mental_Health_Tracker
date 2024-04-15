from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from django.urls import reverse
from .models import JournalEntry, SubstanceAbuseTracking, Article, Videos, Therapist
from datetime import datetime
from django.core import mail
from unittest.mock import patch
from django.conf import settings as django_settings
import json


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

    self.therapist = Therapist.objects.create(
        user=self.user,
        first_name="John",
        last_name="Doe",
        email="jd@mail.com",
        company="Therapy Inc.",
        phone_number="123-456-7890",
    )

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
    response = self.client.get(reverse('reports'))
    self.assertEqual(response.status_code, 200)


class JournalEntryTestCase(TestCase):

  def setUp(self):
    #Create a User
    self.user = User.objects.create_user(username='testuser', password='12345')
    self.client.login(username='testuser', password='12345')

  def test_journal_entry(self):
    #Information the sent back from the form
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

    #Assert that when this information is sent back from the form
    #A journal entry is saved
    self.client.post(reverse('journal_entry'), request)
    self.assertTrue(JournalEntry.objects.filter(user=self.user).exists())


class ReportsTestCase(TestCase):

  def setUp(self):
    #Creates a User
    self.user = User.objects.create_user(username='testuser', password='12345')
    self.client.login(username='testuser', password='12345')

  def test_report_single_positive(self):
    #Creates a positive Journal Entry
    self.journal_entry = JournalEntry.objects.create(user=self.user,
                                                     mood_level=5,
                                                     sleep_quality=4,
                                                     exercise_time=60,
                                                     diet_quality=2,
                                                     water_intake=7,
                                                     journal_text="Test entry")

    #Gather the response of the Template after calling the Template
    response = self.client.get(reverse('reports'), '')

    #Assert the values in context are sent in correctly to calc stats
    self.assertEqual(response.context['mood_negative'], 0)
    self.assertEqual(response.context['sleepAvg_negative'], 0)
    self.assertEqual(response.context['exerciseAvg_negative'], 0)
    self.assertEqual(response.context['dietAvg_negative'], 0)
    self.assertEqual(response.context['waterAvg_negative'], 0)
    self.assertEqual(response.context['journalAvg_negative'], 'not')
    self.assertEqual(response.context['mood_neutral'], 0)
    self.assertEqual(response.context['mood_positive'], 1)
    self.assertEqual(response.context['sleepAvg_positive'], 4)
    self.assertEqual(response.context['exerciseAvg_positive'], 60)
    self.assertEqual(response.context['dietAvg_positive'], 2)
    self.assertEqual(response.context['waterAvg_positive'], 7)
    self.assertEqual(response.context['journalAvg_positive'], '')
    self.assertEqual(response.context['sleep_negative'], 0)
    self.assertEqual(response.context['sleep_neutral'], 0)
    self.assertEqual(response.context['sleep_positive'], 1)
    self.assertEqual(response.context['exercise_negative'], 0)
    self.assertEqual(response.context['exercise_positive'], 1)
    self.assertEqual(response.context['diet_negative'], 1)
    self.assertEqual(response.context['diet_neutral'], 0)
    self.assertEqual(response.context['diet_positive'], 0)
    self.assertEqual(response.context['water_negative'], 1)
    self.assertEqual(response.context['water_positive'], 0)
    self.assertEqual(response.context['journal_entries_negative'], 0)
    self.assertEqual(response.context['journal_entries_positive'], 1)

  def test_report_single_negative(self):
    #Creates a negative Journal Entry
    self.journal_entry = JournalEntry.objects.create(user=self.user,
                                                     mood_level=2,
                                                     sleep_quality=2,
                                                     exercise_time=45,
                                                     diet_quality=4,
                                                     water_intake=10,
                                                     journal_text="")

    #Gather the response of the Template after calling the Template
    response = self.client.get(reverse('reports'), '')

    #Assert the values in context are sent in correctly to calc stats
    self.assertEqual(response.context['mood_negative'], 1)
    self.assertEqual(response.context['sleepAvg_negative'], 2)
    self.assertEqual(response.context['exerciseAvg_negative'], 45)
    self.assertEqual(response.context['dietAvg_negative'], 4)
    self.assertEqual(response.context['waterAvg_negative'], 10)
    self.assertEqual(response.context['journalAvg_negative'], 'not')
    self.assertEqual(response.context['mood_neutral'], 0)
    self.assertEqual(response.context['mood_positive'], 0)
    self.assertEqual(response.context['sleepAvg_positive'], 0)
    self.assertEqual(response.context['exerciseAvg_positive'], 0)
    self.assertEqual(response.context['dietAvg_positive'], 0)
    self.assertEqual(response.context['waterAvg_positive'], 0)
    self.assertEqual(response.context['journalAvg_positive'], 'not')
    self.assertEqual(response.context['sleep_negative'], 1)
    self.assertEqual(response.context['sleep_neutral'], 0)
    self.assertEqual(response.context['sleep_positive'], 0)
    self.assertEqual(response.context['exercise_negative'], 1)
    self.assertEqual(response.context['exercise_positive'], 0)
    self.assertEqual(response.context['diet_negative'], 0)
    self.assertEqual(response.context['diet_neutral'], 0)
    self.assertEqual(response.context['diet_positive'], 1)
    self.assertEqual(response.context['water_negative'], 0)
    self.assertEqual(response.context['water_positive'], 1)
    self.assertEqual(response.context['journal_entries_negative'], 1)
    self.assertEqual(response.context['journal_entries_positive'], 0)

  def test_report_double(self):
    #Creates two objects one negative and one positive
    self.journal_entry = JournalEntry.objects.create(user=self.user,
                                                     mood_level=1,
                                                     sleep_quality=2,
                                                     exercise_time=30,
                                                     diet_quality=2,
                                                     water_intake=3,
                                                     journal_text="")

    self.journal_entry = JournalEntry.objects.create(user=self.user,
                                                     mood_level=5,
                                                     sleep_quality=4,
                                                     exercise_time=60,
                                                     diet_quality=4,
                                                     water_intake=10,
                                                     journal_text="Test")

    #Gather the response of the Template after calling the Template
    response = self.client.get(reverse('reports'), '')

    #Assert the values in context are sent in correctly to calc stats
    self.assertEqual(response.context['mood_negative'], 1)
    self.assertEqual(response.context['sleepAvg_negative'], 2)
    self.assertEqual(response.context['exerciseAvg_negative'], 30)
    self.assertEqual(response.context['dietAvg_negative'], 2)
    self.assertEqual(response.context['waterAvg_negative'], 3)
    self.assertEqual(response.context['journalAvg_negative'], 'not')
    self.assertEqual(response.context['mood_neutral'], 0)
    self.assertEqual(response.context['mood_positive'], 1)
    self.assertEqual(response.context['sleepAvg_positive'], 4)
    self.assertEqual(response.context['exerciseAvg_positive'], 60)
    self.assertEqual(response.context['dietAvg_positive'], 4)
    self.assertEqual(response.context['waterAvg_positive'], 10)
    self.assertEqual(response.context['journalAvg_positive'], '')
    self.assertEqual(response.context['sleep_negative'], 1)
    self.assertEqual(response.context['sleep_neutral'], 0)
    self.assertEqual(response.context['sleep_positive'], 1)
    self.assertEqual(response.context['exercise_negative'], 1)
    self.assertEqual(response.context['exercise_positive'], 1)
    self.assertEqual(response.context['diet_negative'], 1)
    self.assertEqual(response.context['diet_neutral'], 0)
    self.assertEqual(response.context['diet_positive'], 1)
    self.assertEqual(response.context['water_negative'], 1)
    self.assertEqual(response.context['water_positive'], 1)
    self.assertEqual(response.context['journal_entries_negative'], 1)
    self.assertEqual(response.context['journal_entries_positive'], 1)

  def test_report_no_entries(self):
    #Creates no objects for the reports to draw from

    #Gathers the response from the GET
    response = self.client.get(reverse('reports'), '')

    #Asserts that the values in context are sent in correctly to calc stats
    self.assertEqual(response.context['mood_negative'], 0)
    self.assertEqual(response.context['sleepAvg_negative'], 0)
    self.assertEqual(response.context['exerciseAvg_negative'], 0)
    self.assertEqual(response.context['dietAvg_negative'], 0)
    self.assertEqual(response.context['waterAvg_negative'], 0)
    self.assertEqual(response.context['journalAvg_negative'], 'not')
    self.assertEqual(response.context['mood_neutral'], 0)
    self.assertEqual(response.context['mood_positive'], 0)
    self.assertEqual(response.context['sleepAvg_positive'], 0)
    self.assertEqual(response.context['exerciseAvg_positive'], 0)
    self.assertEqual(response.context['dietAvg_positive'], 0)
    self.assertEqual(response.context['waterAvg_positive'], 0)
    self.assertEqual(response.context['journalAvg_positive'], 'not')
    self.assertEqual(response.context['sleep_negative'], 0)
    self.assertEqual(response.context['sleep_neutral'], 0)
    self.assertEqual(response.context['sleep_positive'], 0)
    self.assertEqual(response.context['exercise_negative'], 0)
    self.assertEqual(response.context['exercise_positive'], 0)
    self.assertEqual(response.context['diet_negative'], 0)
    self.assertEqual(response.context['diet_neutral'], 0)
    self.assertEqual(response.context['diet_positive'], 0)
    self.assertEqual(response.context['water_negative'], 0)
    self.assertEqual(response.context['water_positive'], 0)
    self.assertEqual(response.context['journal_entries_negative'], 0)
    self.assertEqual(response.context['journal_entries_positive'], 0)

  @patch('mh_tracker.views.send_mail')
  def test_email_user(self, mock_send_mail):
    # Set up mock behavior
    mock_send_mail.return_value = 1  # Assuming 1 means success
    data = {'Subject': 'Test Subject', 'Message': 'Test Message'}
    json_data = json.dumps(data)

    # Trigger the code that sends the email
    response = self.client.post(reverse('send_email_self'),
                                content_type='application/json',
                                data=json_data)

    # Assert that send_mail was called with the expected arguments
    mock_send_mail.assert_called_once_with(
        'Test Subject',
        'Test Message',
        django_settings.EMAIL_HOST_USER_2, [self.user.email],
        fail_silently=False,
        auth_user=django_settings.EMAIL_HOST_USER_2,
        auth_password=django_settings.EMAIL_HOST_PASSWORD_2)

    # Assert that the email was not actually sent
    self.assertEqual(len(mail.outbox), 0)
