from django.urls import path
from . import api_views

urlpatterns = [
    path('greenhouses/', api_views.greenhouse_list_api, name='api_greenhouses'),
    path('sensor-data/<int:greenhouse_id>/', api_views.sensor_data_api, name='api_sensor_data'),
    path('sensor-data/upload/', api_views.sensor_data_upload, name='api_sensor_upload'),
    path('chart-data/<int:greenhouse_id>/', api_views.chart_data_api, name='api_chart_data'),
]
