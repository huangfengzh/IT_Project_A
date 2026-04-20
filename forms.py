from django import forms
from .models import AlertRule


class AlertRuleForm(forms.ModelForm):
    """Form for creating and editing alert rules."""

    class Meta:
        model = AlertRule
        fields = ['greenhouse', 'metric', 'condition', 'threshold_value', 'severity']
        widgets = {
            'greenhouse': forms.Select(attrs={'class': 'form-select'}),
            'metric': forms.Select(attrs={'class': 'form-select'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'threshold_value': forms.NumberInput(attrs={
                'class': 'form-control', 'step': '0.1',
            }),
            'severity': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from monitoring.models import Greenhouse
        self.fields['greenhouse'].queryset = Greenhouse.objects.filter(owner=user)
