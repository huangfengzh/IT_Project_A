from django.urls import path
from . import views

app_name = 'alerts'

urlpatterns = [
    path('', views.alert_list, name='alert_list'),
    path('create/', views.create_alert_rule, name='create_rule'),
    path('delete/<int:pk>/', views.delete_alert_rule, name='delete_rule'),
    path('resolve/<int:pk>/', views.resolve_alert, name='resolve_alert'),
]
