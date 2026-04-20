from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Greenhouse, SensorReading


class GreenhouseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.greenhouse = Greenhouse.objects.create(
            name='Test Greenhouse', location='Lab A', owner=self.user
        )

    def test_greenhouse_str(self):
        self.assertEqual(str(self.greenhouse), 'Test Greenhouse')

    def test_latest_reading_none(self):
        self.assertIsNone(self.greenhouse.latest_reading())

    def test_latest_reading(self):
        reading = SensorReading.objects.create(
            greenhouse=self.greenhouse,
            temperature=25.5, humidity=60.0,
            soil_moisture=45.0, light_intensity=800.0,
        )
        self.assertEqual(self.greenhouse.latest_reading(), reading)


class DashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass123')

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('monitoring:dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_loads(self):
        self.client.login(username='testuser', password='pass123')
        response = self.client.get(reverse('monitoring:dashboard'))
        self.assertEqual(response.status_code, 200)


class SensorReadingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.greenhouse = Greenhouse.objects.create(name='Test GH', owner=self.user)

    def test_reading_creation(self):
        reading = SensorReading.objects.create(
            greenhouse=self.greenhouse,
            temperature=22.5, humidity=55.0,
            soil_moisture=40.0, light_intensity=600.0,
        )
        self.assertIn('Test GH', str(reading))
