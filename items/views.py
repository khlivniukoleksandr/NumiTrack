from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from items.models import (Collector,
                          Collection)


def index(request: HttpRequest) -> HttpResponse:
    count_users = Collector.objects.count()
    count_collections = Collection.objects.count()
    context = {
        "count_users": count_users,
        "count_collections": count_collections,
    }
    return render(request, "home_page.html", context)
