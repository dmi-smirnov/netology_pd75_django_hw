import time
import os

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse


def home_view(request):
    template_name = 'app/home.html'
    # впишите правильные адреса страниц, используя
    # функцию `reverse`
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }
    
    # context и параметры render менять не нужно
    # подбробнее о них мы поговорим на следующих лекциях
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    # обратите внимание – здесь HTML шаблона нет, 
    # возвращается просто текст
    current_time = time.strftime('%H:%M:%S', time.localtime())
    msg = f'Текущее время: {current_time}'
    return HttpResponse(msg)


def workdir_view(request):
    template_name = 'app/work_dir.html'
    work_dir_path = os.path.dirname(__file__)
    context = {
        'work_dir_path': work_dir_path,
        'files_list': os.listdir(work_dir_path)
    }
    return render(request, template_name, context)
