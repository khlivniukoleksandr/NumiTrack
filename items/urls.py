from django.urls import path

from items.models import Collection
from items.views import (ProfileView,
                         CollectionListView,
                         CollectionCreateView)

urlpatterns = [
    path("", ProfileView.as_view(), name="profile"),
    path("my-collections/", CollectionListView.as_view(), name="my-collections"),
    path("my-collections/create/", CollectionCreateView.as_view(), name="create-collection"),
]

app_name = "items"
