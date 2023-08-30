from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.conf import settings

from students.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "name", "students")
    
    def validate(self, attrs):
        # Проверяем количество студентов на курсе
        students_field_name = 'students'
        if students_field_name in attrs.keys():
            if len(attrs[students_field_name]) > settings.STUDENTS_MAX_PER_COURSE:
                raise ValidationError(f'Number of students per course'
                                f' must be at most'
                                f' {settings.STUDENTS_MAX_PER_COURSE}')
        return super().validate(attrs)
