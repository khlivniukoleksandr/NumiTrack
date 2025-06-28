from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from items.models import (Collector,
                          Collection,
                          Coin, Banknote
                          )


def index(request: HttpRequest) -> HttpResponse:
    num_coins = Coin.objects.count()
    count_users = Collector.objects.count()
    count_collections = Collection.objects.count()
    num_banknotes = Banknote.objects.count()
    count_collectors = Collector.objects.count()
    num_country = Coin.objects.filter(country__isnull=False).count()
    context = {
        "count_users": count_users,
        "count_collections": count_collections,
        "num_coins": num_coins,
        "num_banknotes": num_banknotes,
        "count_collectors": count_collectors,
        "num_country": num_country,
    }
    return render(request, "home_page.html", context)
