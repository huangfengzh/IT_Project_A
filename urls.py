from django.urls import path
from . import views

app_name = 'monitoring'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('greenhouse/<int:pk>/', views.greenhouse_detail, name='greenhouse_detail'),
    path('greenhouse/<int:pk>/history/', views.history_view, name='history'),
]
