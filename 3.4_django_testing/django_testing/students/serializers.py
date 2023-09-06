from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.conf import settings

from students.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "name", "students")
    
    def validate_students(self, value):
        # Проверяем количество студентов на курсе
        if len(value) > settings.STUDENTS_MAX_PER_COURSE:
            raise ValidationError(
                f'Number of students per course'
                f' must be at most'
                f' {settings.STUDENTS_MAX_PER_COURSE}'
            )
        return value

