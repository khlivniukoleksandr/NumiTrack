from django.urls import path

from items.models import Collection
from items.views import (ProfileView,
                         CollectionListView,
                         CollectionCreateView,
                         CollectionDetailView,
                         CollectionUpdateView,
                         CollectionDeleteView,
                         CoinListView,
                         CoinDetailView,
                         CoinDeleteView,
                         CoinUpdateView,
                         CoinCreateView,
                         AddCoinToCollectionView,
                         BanknoteListView,
                         BanknoteCreateView,
                         BanknoteDetailView,
                         BanknoteUpdateView,
                         BanknoteDeleteView,
                         PublicCollectionListView,
                         AddBanknoteToCollectionView)

urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),

    # Collections

    path("my-collections/", CollectionListView.as_view(), name="my-collections"),
    path("my-collections/detail/<int:pk>/", CollectionDetailView.as_view(), name="collection-detail"),
    path("my-collections/<int:pk>/delete/", CollectionDeleteView.as_view(), name="collection-delete"),
    path("my-collections/<int:pk>/edit/", CollectionUpdateView.as_view(), name="collection-edit"),
    path("my-collections/create/", CollectionCreateView.as_view(), name="create-collection"),
    path("my-collections/<int:pk>/add-coin/", AddCoinToCollectionView.as_view(), name="add-coin-to-collection"),
    path("my-collections/<int:pk>/add-banknote/", AddBanknoteToCollectionView.as_view(), name="add-banknote-to-collection"),

    # Coins

    path("my-coins/", CoinListView.as_view(), name="my-coins"),
    path("my-coins/create", CoinCreateView.as_view(), name="coin-create"),
    path("my-coins/detail/<int:pk>/", CoinDetailView.as_view(), name="coin-detail"),
    path("my-coins/detail/<int:pk>/delete/", CoinDeleteView.as_view(), name="coin-delete"),
    path("my-coins/detail/<int:pk>/edit/", CoinUpdateView.as_view(), name="coin-edit"),

    # Banknotes

    path("my-banknotes/", BanknoteListView.as_view(), name="my-banknotes"),
    path("my-banknotes/create/", BanknoteCreateView.as_view(), name="banknote-create"),
    path("my-banknotes/detail/<int:pk>", BanknoteDetailView.as_view(), name="banknote-detail"),
    path("my-banknotes/<int:pk>/edit", BanknoteUpdateView.as_view(), name="banknote-edit"),
    path("my-banknotes/<int:pk>/delete/", BanknoteDeleteView.as_view(), name="banknote-delete"),

    # All collections

    path("collections/", PublicCollectionListView.as_view(), name="public-collections"),
]

app_name = "items"
