from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import Greenhouse, SensorReading
from .serializers import SensorReadingSerializer, GreenhouseSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def greenhouse_list_api(request):
    """List all greenhouses for the authenticated user."""
    greenhouses = Greenhouse.objects.filter(owner=request.user)
    serializer = GreenhouseSerializer(greenhouses, many=True)
    return Response({'success': True, 'data': serializer.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sensor_data_api(request, greenhouse_id):
    """Get sensor readings for a greenhouse."""
    greenhouse = Greenhouse.objects.filter(pk=greenhouse_id, owner=request.user).first()
    if not greenhouse:
        return Response(
            {'success': False, 'error': 'Greenhouse not found'},
            status=status.HTTP_404_NOT_FOUND,
        )
    hours = int(request.GET.get('hours', 24))
    since = timezone.now() - timedelta(hours=hours)
    readings = SensorReading.objects.filter(
        greenhouse=greenhouse, timestamp__gte=since
    ).order_by('timestamp')
    serializer = SensorReadingSerializer(readings, many=True)
    return Response({'success': True, 'data': serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sensor_data_upload(request):
    """Upload new sensor reading from IoT device."""
    serializer = SensorReadingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {'success': True, 'data': serializer.data},
            status=status.HTTP_201_CREATED,
        )
    return Response(
        {'success': False, 'error': serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chart_data_api(request, greenhouse_id):
    """Get chart-ready data for frontend visualization."""
    greenhouse = Greenhouse.objects.filter(pk=greenhouse_id, owner=request.user).first()
    if not greenhouse:
        return Response(
            {'success': False, 'error': 'Greenhouse not found'},
            status=status.HTTP_404_NOT_FOUND,
        )
    hours = int(request.GET.get('hours', 24))
    since = timezone.now() - timedelta(hours=hours)
    readings = SensorReading.objects.filter(
        greenhouse=greenhouse, timestamp__gte=since
    ).order_by('timestamp').values(
        'timestamp', 'temperature', 'humidity',
        'soil_moisture', 'light_intensity', 'co2_level'
    )
    data = {
        'labels': [r['timestamp'].strftime('%H:%M') for r in readings],
        'temperature': [r['temperature'] for r in readings],
        'humidity': [r['humidity'] for r in readings],
        'soil_moisture': [r['soil_moisture'] for r in readings],
        'light_intensity': [r['light_intensity'] for r in readings],
        'co2_level': [r['co2_level'] for r in readings],
    }
    return Response({'success': True, 'data': data})
