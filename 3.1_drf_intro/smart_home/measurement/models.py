from django.db import models


# TODO: опишите модели датчика (Sensor) и измерения (Measurement)

class Sensor(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return (f'ID: {self.pk} Название: {self.name}'
                f' Описание: {self.description}')

class Measurement(models.Model):
    sensor_id = models.ForeignKey(Sensor, on_delete=models.CASCADE,
                                  to_field='id', related_name='measurements')
    temp = models.DecimalField(max_digits=5, decimal_places=2)
    datetime = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(null=True, blank=True)