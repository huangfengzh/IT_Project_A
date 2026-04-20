from rest_framework import serializers
from .models import Greenhouse, SensorReading


class SensorReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorReading
        fields = [
            'id', 'greenhouse', 'temperature', 'humidity',
            'soil_moisture', 'light_intensity', 'co2_level', 'timestamp',
        ]
        read_only_fields = ['id', 'timestamp']


class GreenhouseSerializer(serializers.ModelSerializer):
    latest_reading = serializers.SerializerMethodField()

    class Meta:
        model = Greenhouse
        fields = ['id', 'name', 'location', 'description', 'is_active', 'latest_reading']

    def get_latest_reading(self, obj):
        reading = obj.latest_reading()
        if reading:
            return SensorReadingSerializer(reading).data
        return None
