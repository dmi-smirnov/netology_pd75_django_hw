from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django_testing.settings import STUDENTS_MAX_PER_COURSE

from students.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "name", "students")
    
    def validate(self, attrs):
        # Проверяем количество студентов на курсе
        students_field_name = 'students'
        if students_field_name in attrs.keys():
            if len(attrs[students_field_name]) > STUDENTS_MAX_PER_COURSE:
                ValidationError(f'Number of students per course'
                                f' must be at most {STUDENTS_MAX_PER_COURSE}')
        return super().validate(attrs)
