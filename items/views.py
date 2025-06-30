from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic
from django.views.generic import FormView

from items.forms import CustomCollectionForm
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

class ProfileView(LoginRequiredMixin, generic.DetailView):
    model = Collector
    template_name = "profile/profile_detail.html"
    context_object_name = "collector"

    def get_object(self, queryset=None):
        return self.request.user


class CollectionListView(LoginRequiredMixin, generic.ListView):
    model = Collection
    template_name = "collections/my_collections.html"
    context_object_name = "collections"

    def get_queryset(self):
        return Collection.objects.filter(owner=self.request.user)




class CollectionCreateView(LoginRequiredMixin, FormView):
    template_name = "collections/collection_form.html"
    form_class = CustomCollectionForm
    success_url = "/profile/my-collections/"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        Collection.objects.create(owner=self.request.user,
                                  name=form.cleaned_data["name"],
                                  description=form.cleaned_data["description"],
                                  cover=form.cleaned_data["cover"]
        )
        return super().form_valid(form)