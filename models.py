from django.db import models
from django.contrib.auth.models import User
from monitoring.models import Greenhouse


class AlertRule(models.Model):
    """Defines threshold rules for sensor data alerts."""

    METRIC_CHOICES = [
        ('temperature', 'Temperature'),
        ('humidity', 'Humidity'),
        ('soil_moisture', 'Soil Moisture'),
        ('light_intensity', 'Light Intensity'),
        ('co2_level', 'CO2 Level'),
    ]
    CONDITION_CHOICES = [
        ('above', 'Above'),
        ('below', 'Below'),
    ]
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    greenhouse = models.ForeignKey(
        Greenhouse, on_delete=models.CASCADE, related_name='alert_rules'
    )
    metric = models.CharField(max_length=20, choices=METRIC_CHOICES)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    threshold_value = models.FloatField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='medium')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return (
            f"{self.greenhouse.name}: {self.get_metric_display()} "
            f"{self.get_condition_display()} {self.threshold_value}"
        )

    def check_reading(self, reading):
        """Check if a sensor reading triggers this alert rule."""
        value = getattr(reading, self.metric, None)
        if value is None:
            return False
        if self.condition == 'above':
            return value > self.threshold_value
        return value < self.threshold_value


class AlertLog(models.Model):
    """Records triggered alerts."""

    alert_rule = models.ForeignKey(
        AlertRule, on_delete=models.CASCADE, related_name='logs'
    )
    greenhouse = models.ForeignKey(
        Greenhouse, on_delete=models.CASCADE, related_name='alert_logs'
    )
    triggered_value = models.FloatField()
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        status = 'Resolved' if self.is_resolved else 'Active'
        return f"[{status}] {self.greenhouse.name}: {self.message[:50]}"
