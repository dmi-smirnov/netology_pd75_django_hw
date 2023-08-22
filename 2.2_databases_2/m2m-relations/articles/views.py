from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.db.models import Prefetch

from articles.models import Article


def articles_list(request: HttpRequest) -> HttpResponse:
    template = 'articles/news.html'

    # используйте этот параметр для упорядочивания результатов
    # https://docs.djangoproject.com/en/3.1/ref/models/querysets/#django.db.models.query.QuerySet.order_by
    ordering = 'published_at'

    articles = Article.objects.prefetch_related('scopes__tag').all().order_by(ordering)

    context = {
        'object_list': articles
    }

    return render(request, template, context)
