from django.contrib import admin
from .models import AlertRule, AlertLog


@admin.register(AlertRule)
class AlertRuleAdmin(admin.ModelAdmin):
    list_display = [
        'greenhouse', 'metric', 'condition',
        'threshold_value', 'severity', 'is_active',
    ]
    list_filter = ['metric', 'severity', 'is_active']


@admin.register(AlertLog)
class AlertLogAdmin(admin.ModelAdmin):
    list_display = [
        'greenhouse', 'alert_rule', 'triggered_value',
        'is_resolved', 'created_at',
    ]
    list_filter = ['is_resolved', 'created_at']
