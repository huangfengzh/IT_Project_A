from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from monitoring.models import Greenhouse, SensorReading
from .models import AlertRule, AlertLog


class AlertRuleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.greenhouse = Greenhouse.objects.create(name='Test GH', owner=self.user)
        self.rule = AlertRule.objects.create(
            greenhouse=self.greenhouse, metric='temperature',
            condition='above', threshold_value=35.0,
            severity='high', created_by=self.user,
        )

    def test_rule_str(self):
        self.assertIn('Temperature', str(self.rule))

    def test_check_reading_triggers(self):
        reading = SensorReading.objects.create(
            greenhouse=self.greenhouse, temperature=40.0,
            humidity=50.0, soil_moisture=40.0, light_intensity=500.0,
        )
        self.assertTrue(self.rule.check_reading(reading))

    def test_check_reading_no_trigger(self):
        reading = SensorReading.objects.create(
            greenhouse=self.greenhouse, temperature=30.0,
            humidity=50.0, soil_moisture=40.0, light_intensity=500.0,
        )
        self.assertFalse(self.rule.check_reading(reading))


class AlertViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass123')

    def test_alert_list_requires_login(self):
        response = self.client.get(reverse('alerts:alert_list'))
        self.assertEqual(response.status_code, 302)

    def test_alert_list_loads(self):
        self.client.login(username='testuser', password='pass123')
        response = self.client.get(reverse('alerts:alert_list'))
        self.assertEqual(response.status_code, 200)
