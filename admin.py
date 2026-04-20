from django.contrib import admin
from .models import Greenhouse, SensorReading


@admin.register(Greenhouse)
class GreenhouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'owner', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'location', 'owner__username']


@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = [
        'greenhouse', 'temperature', 'humidity',
        'soil_moisture', 'light_intensity', 'timestamp',
    ]
    list_filter = ['greenhouse', 'timestamp']
    date_hierarchy = 'timestamp'
