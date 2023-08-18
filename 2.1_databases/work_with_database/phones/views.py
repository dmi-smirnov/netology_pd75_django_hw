from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from phones.models import Phone


def index(request: HttpRequest) -> HttpResponse:
    return redirect('catalog')


def show_catalog(request: HttpRequest) -> HttpResponse:
    sort_param = request.GET.get('sort')
    if sort_param:
        if sort_param == 'name':
            phones = Phone.objects.order_by('name')
        elif sort_param == 'min_price':
            phones = Phone.objects.order_by('price')
        elif sort_param == 'max_price':
            phones = reversed(Phone.objects.order_by('price'))
        else:
            phones = Phone.objects.all()    
    else:
        phones = Phone.objects.all()
    template = 'catalog.html'
    context = {'phones': phones}
    return render(request, template, context)


def show_product(request: HttpRequest, slug: str) -> HttpResponse:
    template = 'product.html'
    context = {'phone': Phone.objects.get(slug=slug)}
    return render(request, template, context)
