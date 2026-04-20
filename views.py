from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Avg, Max, Min
from datetime import timedelta
from .models import Greenhouse, SensorReading
from alerts.models import AlertRule, AlertLog


@login_required
def dashboard(request):
    """Main dashboard showing all greenhouses with latest readings."""
    greenhouses = Greenhouse.objects.filter(
        owner=request.user, is_active=True
    ).prefetch_related('sensor_readings')

    greenhouse_data = []
    for gh in greenhouses:
        latest = gh.latest_reading()
        active_alerts = AlertLog.objects.filter(
            greenhouse=gh, is_resolved=False
        ).count()
        greenhouse_data.append({
            'greenhouse': gh,
            'latest_reading': latest,
            'active_alerts': active_alerts,
        })

    total_greenhouses = greenhouses.count()
    total_alerts = AlertLog.objects.filter(
        greenhouse__owner=request.user, is_resolved=False
    ).count()

    context = {
        'greenhouse_data': greenhouse_data,
        'total_greenhouses': total_greenhouses,
        'total_alerts': total_alerts,
    }
    return render(request, 'monitoring/dashboard.html', context)


@login_required
def greenhouse_detail(request, pk):
    """Detailed view for a single greenhouse."""
    greenhouse = get_object_or_404(Greenhouse, pk=pk, owner=request.user)
    latest = greenhouse.latest_reading()

    since = timezone.now() - timedelta(hours=24)
    stats = greenhouse.sensor_readings.filter(timestamp__gte=since).aggregate(
        avg_temp=Avg('temperature'),
        max_temp=Max('temperature'),
        min_temp=Min('temperature'),
        avg_humidity=Avg('humidity'),
        avg_soil=Avg('soil_moisture'),
        avg_light=Avg('light_intensity'),
    )

    alert_rules = AlertRule.objects.filter(greenhouse=greenhouse)
    recent_alerts = AlertLog.objects.filter(greenhouse=greenhouse)[:10]

    context = {
        'greenhouse': greenhouse,
        'latest': latest,
        'stats': stats,
        'alert_rules': alert_rules,
        'recent_alerts': recent_alerts,
    }
    return render(request, 'monitoring/greenhouse_detail.html', context)


@login_required
def history_view(request, pk):
    """Historical data view with date range filtering."""
    greenhouse = get_object_or_404(Greenhouse, pk=pk, owner=request.user)
    days = int(request.GET.get('days', 7))
    since = timezone.now() - timedelta(days=days)
    readings = greenhouse.sensor_readings.filter(
        timestamp__gte=since
    ).order_by('timestamp')

    context = {
        'greenhouse': greenhouse,
        'readings': readings,
        'days': days,
        'hours': days * 24,
    }
    return render(request, 'monitoring/history.html', context)
