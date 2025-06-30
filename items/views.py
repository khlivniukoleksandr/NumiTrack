from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import FormView, UpdateView, CreateView, DeleteView

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




class CollectionCreateView(LoginRequiredMixin, CreateView):
    model = Collection
    form_class = CustomCollectionForm
    template_name = "collections/collection_form.html"
    success_url = "/profile/my-collections/"

    def form_valid(self, form):
        # Автоматично встановлюємо власника перед збереженням
        form.instance.owner = self.request.user
        return super().form_valid(form)

class CollectionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Collection
    template_name = "collections/collection_detail.html"


class CollectionUpdateView(LoginRequiredMixin, UpdateView):
    model = Collection
    form_class = CustomCollectionForm
    template_name = "collections/collection_form.html"
    success_url = "/profile/my-collections/"

    def get_queryset(self):
        return Collection.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collection'] = self.object  # або self.get_object()
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Collection, pk=self.kwargs["pk"], owner=self.request.user)

class CollectionDeleteView(LoginRequiredMixin, DeleteView):
    model = Collection
    template_name = "collections/collection_confirm_delete.html"
    success_url = reverse_lazy('items:my-collections')

    def get_queryset(self):
        return Collection.objects.filter(owner=self.request.user)

    def get_object(self, queryset=None):
        return get_object_or_404(Collection, pk=self.kwargs["pk"], owner=self.request.user)