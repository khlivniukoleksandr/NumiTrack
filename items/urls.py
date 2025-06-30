from django.urls import path

from items.models import Collection
from items.views import (ProfileView,
                         CollectionListView,
                         CollectionCreateView,
                         CollectionDetailView,
                         CollectionUpdateView,
                         CollectionDeleteView)

urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("my-collections/", CollectionListView.as_view(), name="my-collections"),
    path("my-collections/detail/<int:pk>/", CollectionDetailView.as_view(), name="collection-detail"),
    path("my-collections/<int:pk>/delete/", CollectionDeleteView.as_view(), name="collection-delete"),
    path("my-collections/<int:pk>/edit/", CollectionUpdateView.as_view(), name="collection-edit"),
    path("my-collections/create/", CollectionCreateView.as_view(), name="create-collection"),
]

app_name = "items"
