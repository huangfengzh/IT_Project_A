from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import AlertRule, AlertLog
from .forms import AlertRuleForm


@login_required
def alert_list(request):
    """List all alerts and alert rules."""
    rules = AlertRule.objects.filter(greenhouse__owner=request.user)
    active_alerts = AlertLog.objects.filter(
        greenhouse__owner=request.user, is_resolved=False
    )
    resolved_alerts = AlertLog.objects.filter(
        greenhouse__owner=request.user, is_resolved=True
    )[:20]
    context = {
        'rules': rules,
        'active_alerts': active_alerts,
        'resolved_alerts': resolved_alerts,
    }
    return render(request, 'alerts/alert_list.html', context)


@login_required
def create_alert_rule(request):
    """Create a new alert rule."""
    if request.method == 'POST':
        form = AlertRuleForm(request.user, request.POST)
        if form.is_valid():
            rule = form.save(commit=False)
            rule.created_by = request.user
            rule.save()
            messages.success(request, 'Alert rule created successfully.')
            return redirect('alerts:alert_list')
    else:
        form = AlertRuleForm(request.user)
    return render(request, 'alerts/create_rule.html', {'form': form})


@login_required
def delete_alert_rule(request, pk):
    """Delete an alert rule."""
    rule = get_object_or_404(AlertRule, pk=pk, greenhouse__owner=request.user)
    if request.method == 'POST':
        rule.delete()
        messages.success(request, 'Alert rule deleted.')
        return redirect('alerts:alert_list')
    return render(request, 'alerts/confirm_delete.html', {'rule': rule})


@login_required
def resolve_alert(request, pk):
    """Resolve an active alert."""
    alert = get_object_or_404(
        AlertLog, pk=pk, greenhouse__owner=request.user, is_resolved=False
    )
    if request.method == 'POST':
        alert.is_resolved = True
        alert.resolved_at = timezone.now()
        alert.resolved_by = request.user
        alert.save()
        messages.success(request, 'Alert resolved successfully.')
    return redirect('alerts:alert_list')
