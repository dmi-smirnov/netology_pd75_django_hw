import csv

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.core.paginator import Paginator


def index(request: HttpRequest) -> HttpResponse:
    return redirect(reverse('bus_stations'))


def bus_stations(request: HttpRequest) -> HttpResponse:
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    with open(settings.BUS_STATION_CSV) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        csv_data = [row_dict for row_dict in csv_reader]

    paginator = Paginator(csv_data, 10)
    page_number = int(request.GET.get('page', 1))
    page = paginator.get_page(page_number)

    context = {
        'bus_stations': page.object_list,
        'page': page
    }

    return render(request, 'stations/index.html', context)
