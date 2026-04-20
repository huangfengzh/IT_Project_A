from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Greenhouse(models.Model):
    """Represents a physical greenhouse unit."""

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200, blank=True, default='')
    description = models.TextField(blank=True, default='')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='greenhouses')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def latest_reading(self):
        return self.sensor_readings.order_by('-timestamp').first()


class SensorReading(models.Model):
    """Records sensor data from a greenhouse at a point in time."""

    greenhouse = models.ForeignKey(
        Greenhouse, on_delete=models.CASCADE, related_name='sensor_readings'
    )
    temperature = models.FloatField(help_text='Temperature in Celsius')
    humidity = models.FloatField(help_text='Relative humidity in %')
    soil_moisture = models.FloatField(help_text='Soil moisture in %')
    light_intensity = models.FloatField(help_text='Light intensity in lux')
    co2_level = models.FloatField(default=400.0, help_text='CO2 level in ppm')
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['greenhouse', '-timestamp']),
        ]

    def __str__(self):
        return (
            f"{self.greenhouse.name} - "
            f"T:{self.temperature}C H:{self.humidity}% "
            f"@ {self.timestamp:%Y-%m-%d %H:%M}"
        )
