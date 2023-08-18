from datetime import datetime

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator

from books.models import Book


def redirect_to_books(request: HttpRequest) -> HttpResponse:
    return redirect(reverse('books'))

def books_view(request: HttpRequest) -> HttpResponse:
    template = 'books/books_list.html'
    context = {'books': Book.objects.all()}
    return render(request, template, context)

def book_view(request: HttpRequest, book_id: int) -> HttpResponse:
    template = 'books/books_list.html'
    context = {'books': Book.objects.filter(id=book_id)}
    return render(request, template, context)

def books_view_by_date(request: HttpRequest, pub_date: str) -> HttpResponse:
    template = 'books/books_list.html'

    books = Book.objects.filter(pub_date=pub_date)
    prev_pub_date = None
    next_pub_date = None
    if books:
        books_pub_dates_turples =\
            Book.objects.order_by('pub_date').values_list('pub_date').distinct()
        books_pub_dates = [t[0] for t in books_pub_dates_turples]
        pub_date_index =\
            books_pub_dates.index(datetime.strptime(pub_date, '%Y-%m-%d').date())
        if pub_date_index > 0:
            prev_pub_date = books_pub_dates[pub_date_index - 1]
        if pub_date_index + 1 < len(books_pub_dates):
            next_pub_date = books_pub_dates[pub_date_index + 1]

    context = {
        'books': books,
        'by_date': True,
        'prev_pub_date': prev_pub_date,
        'next_pub_date': next_pub_date
    }

    return render(request, template, context)