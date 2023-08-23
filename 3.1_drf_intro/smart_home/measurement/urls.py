from django.urls import path

from measurement.views import MeasurementAPIView, SensorAPIView, SensorsAPIView


urlpatterns = [
    # TODO: зарегистрируйте необходимые маршруты
    path('sensors/', SensorsAPIView.as_view()),
    path('sensors/<pk>', SensorAPIView.as_view()),
    path('measurements', MeasurementAPIView.as_view())
]