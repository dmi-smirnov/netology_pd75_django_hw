# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView


from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from measurement.models import Measurement, Sensor
from measurement.serializers import MeasurementSerializer, SensorBriefSerializer, SensorSerializer


class SensorsAPIView(ListAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorBriefSerializer

    def post(self, request: Request) -> Response:
        if not isinstance(request.POST, dict):
            raise ValidationError()
        
        sensor_name = request.POST.get('name')
        if not sensor_name:
            raise ValidationError('Field "name" may not be blank.')
        
        sensor_descr = request.POST.get('description')

        new_sensor =\
            Sensor.objects.create(name=sensor_name, description=sensor_descr)
        resp_data = SensorSerializer(new_sensor).data

        return Response(status=201, data=resp_data)
    
class SensorAPIView(RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    def patch(self, request: Request, pk: str) -> Response:
        if not isinstance(request.data, dict):
            raise ValidationError('Request data must be json')
        
        sensor_name = request.data.get('name')
        if sensor_name == '':
            raise ValidationError('Field "name" may not be blank.')
        
        return super().patch(request, pk)

class MeasurementAPIView(CreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer