from rest_framework import serializers

from measurement.models import Measurement, Sensor


# TODO: опишите необходимые сериализаторы

class SensorBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description']

class MeasurementBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['temp', 'datetime', 'img']

class SensorSerializer(serializers.ModelSerializer):
    measurements = MeasurementBriefSerializer(read_only=True, many=True)

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements']

class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['sensor_id', 'temp', 'datetime', 'img']