from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import UpdateView, CreateView, DeleteView, ListView

from items.forms import (CustomCollectionForm,
                         CustomCoinForm,
                         CustomBanknoteForm,
                         CoinFilterForm,
                         CollectionFilterForm,
                         BanknoteFilterForm)
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
    num_country = Coin.objects.filter(country__isnull=False).values('country').distinct().count()

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["edit_mode"] = self.request.GET.get("edit") == "true"
        return context

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.bio = request.POST.get("bio", user.bio)
        user.save()
        return redirect("items:profile")


class CollectionListView(LoginRequiredMixin, generic.ListView):
    model = Collection
    template_name = "collections/my_collections.html"
    context_object_name = "collections"
    paginate_by = 12

    def get_queryset(self):
        queryset = Collection.objects.filter(owner=self.request.user)
        name = self.request.GET.get("name")
        description = self.request.GET.get("description")
        if name:
            queryset = queryset.filter(name__icontains=name)
        if description:
            queryset = queryset.filter(description__icontains=description)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CollectionFilterForm(self.request.GET or None)
        return context



class CollectionCreateView(LoginRequiredMixin, CreateView):
    model = Collection
    form_class = CustomCollectionForm
    template_name = "collections/collection_form.html"
    success_url = reverse_lazy("items:my-collections")

    def form_valid(self, form):

        form.instance.owner = self.request.user
        return super().form_valid(form)

class CollectionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Collection
    template_name = "collections/collection_detail.html"




class CollectionUpdateView(LoginRequiredMixin, UpdateView):
    model = Collection
    form_class = CustomCollectionForm
    template_name = "collections/collection_form.html"
    success_url = reverse_lazy("items:my-collections")

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


class AddCoinToCollectionView(LoginRequiredMixin, ListView):
    template_name = "collections/add_coin_to_collection.html"
    context_object_name = "available_coins"
    paginate_by = 15

    def get_queryset(self):
        collection_pk = self.kwargs["pk"]
        self.collection = get_object_or_404(Collection, pk=collection_pk, owner=self.request.user)

        queryset = self.request.user.coins.exclude(
            pk__in=self.collection.coins.values_list("pk", flat=True)
        )

        self.form = CoinFilterForm(self.request.GET)
        if self.form.is_valid():
            name = self.form.cleaned_data.get("name")
            year = self.form.cleaned_data.get("year")
            country = self.form.cleaned_data.get("country")
            material = self.form.cleaned_data.get("material")

            if name:
                queryset = queryset.filter(name__icontains=name)
            if year:
                queryset = queryset.filter(year__icontains=year)
            if country:
                queryset = queryset.filter(country__icontains=country)
            if material:
                queryset = queryset.filter(material__icontains=material)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["collection"] = self.collection
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        collection = get_object_or_404(Collection, pk=self.kwargs["pk"], owner=self.request.user)
        coin_id = request.POST.get("coin_id")
        if coin_id:
            coin = get_object_or_404(Coin, pk=coin_id, owner=request.user)
            collection.coins.add(coin)
        return redirect("items:add-coin-to-collection", pk=collection.pk)



class AddBanknoteToCollectionView(LoginRequiredMixin, ListView):
    template_name = "collections/add_banknote_to_collection.html"
    context_object_name = "available_banknotes"
    paginate_by = 15

    def get_queryset(self):
        collection_pk = self.kwargs["pk"]
        self.collection = get_object_or_404(Collection, pk=collection_pk, owner=self.request.user)

        queryset = self.request.user.banknotes.exclude(
            pk__in=self.collection.banknotes.values_list("pk", flat=True)
        )

        self.form = BanknoteFilterForm(self.request.GET)
        if self.form.is_valid():
            name = self.form.cleaned_data.get("name")
            year = self.form.cleaned_data.get("year")
            country = self.form.cleaned_data.get("country")

            if name:
                queryset = queryset.filter(name__icontains=name)
            if year:
                queryset = queryset.filter(year__icontains=year)
            if country:
                queryset = queryset.filter(country__icontains=country)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["collection"] = self.collection
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        collection = get_object_or_404(Collection, pk=self.kwargs["pk"], owner=self.request.user)
        banknote_id = request.POST.get("banknote_id")
        if banknote_id:
            banknote = get_object_or_404(Banknote, pk=banknote_id, owner=request.user)
            collection.banknotes.add(banknote)
        return redirect("items:add-banknote-to-collection", pk=collection.pk)


class CoinListView(LoginRequiredMixin, generic.ListView):
    model = Coin
    template_name = "coins/my_coins.html"
    context_object_name = "coins"
    paginate_by = 12

    def get_queryset(self):
        queryset = Coin.objects.filter(owner=self.request.user)
        name = self.request.GET.get("name")
        year = self.request.GET.get("year")
        country = self.request.GET.get("country")
        material = self.request.GET.get("material")
        sort_by = self.request.GET.get("sort_by", "year")
        if name:
            queryset = queryset.filter(name__icontains=name)
        if year:
            queryset = queryset.filter(year__icontains=year)
        if country:
            queryset = queryset.filter(country__icontains=country)
        if material:
            queryset = queryset.filter(material__icontains=material)

        queryset = queryset.order_by(sort_by)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CoinFilterForm(self.request.GET or None)
        return context



class CoinDetailView(LoginRequiredMixin, generic.DetailView):
    model = Coin
    template_name = "coins/coin_detail.html"


class CoinDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Coin
    template_name = "coins/coin_confirm_delete.html"
    success_url = reverse_lazy('items:my-coins')

    def get_queryset(self):
        return Coin.objects.filter(owner=self.request.user)

    def get_object(self, queryset=None):
        return get_object_or_404(Coin, pk=self.kwargs["pk"], owner=self.request.user)

class CoinCreateView(LoginRequiredMixin, CreateView):
    model = Coin
    form_class = CustomCoinForm
    template_name = "coins/coin_form.html"
    success_url = reverse_lazy('items:my-coins')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CoinUpdateView(LoginRequiredMixin, UpdateView):
    model = Coin
    form_class = CustomCoinForm
    template_name = "coins/coin_form.html"
    success_url = reverse_lazy('items:my-coins')

    def get_queryset(self):
        return Coin.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['coin'] = self.object
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Coin, pk=self.kwargs["pk"], owner=self.request.user)


class BanknoteListView(LoginRequiredMixin, generic.ListView):
    model = Banknote
    template_name = "banknotes/my_banknotes.html"
    context_object_name = "banknotes"
    paginate_by = 12

    def get_queryset(self):
        queryset = Banknote.objects.filter(owner=self.request.user)
        name = self.request.GET.get("name")
        year = self.request.GET.get("year")
        country = self.request.GET.get("country")
        sort_by = self.request.GET.get("sort_by", "year")
        if name:
            queryset = queryset.filter(name__icontains=name)
        if year:
            queryset = queryset.filter(year__icontains=year)
        if country:
            queryset = queryset.filter(country__icontains=country)
        queryset = queryset.order_by(sort_by)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BanknoteFilterForm(self.request.GET or None)
        return context


class BanknoteCreateView(LoginRequiredMixin, CreateView):
    form_class = CustomBanknoteForm
    template_name = "banknotes/banknote_form.html"
    success_url = reverse_lazy('items:my-banknotes')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class BanknoteDetailView(LoginRequiredMixin, generic.DetailView):
    model = Banknote
    template_name = "banknotes/banknote_detail.html"


class BanknoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Banknote
    form_class = CustomBanknoteForm
    template_name = "banknotes/banknote_form.html"
    success_url = reverse_lazy('items:my-banknotes')

    def get_queryset(self):
        return Coin.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['banknote'] = self.object
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Banknote, pk=self.kwargs["pk"], owner=self.request.user)


class BanknoteDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Banknote
    template_name = "banknotes/banknote_confirm_delete.html"
    success_url = reverse_lazy('items:my-banknotes')

    def get_queryset(self):
        return Banknote.objects.filter(owner=self.request.user)

    def get_object(self, queryset=None):
        return get_object_or_404(Banknote, pk=self.kwargs["pk"], owner=self.request.user)


class PublicCollectionListView(generic.ListView):
    model = Collection
    template_name = "collections/public_collections.html"
    context_object_name = "public_collections"
    paginate_by = 15

    def get_queryset(self):
        queryset = Collection.objects.all()
        name = self.request.GET.get("name")
        description = self.request.GET.get("description")
        if name:
            queryset = queryset.filter(name__icontains=name)
        if description:
            queryset = queryset.filter(description__icontains=description)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CollectionFilterForm(self.request.GET or None)
        return context


