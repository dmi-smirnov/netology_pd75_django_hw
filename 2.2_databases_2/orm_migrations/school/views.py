from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Student


def students_list(request: HttpRequest) -> HttpResponse:
    template = 'school/students_list.html'

    # используйте этот параметр для упорядочивания результатов
    # https://docs.djangoproject.com/en/2.2/ref/models/querysets/#django.db.models.query.QuerySet.order_by
    ordering = 'group'
    
    context = {
        'object_list': Student.objects.prefetch_related('teachers').all().order_by(ordering)
    }

    return render(request, template, context)
