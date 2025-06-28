from django.urls import path

from items.views import ProfileView

urlpatterns = [
    path("", ProfileView.as_view(), name="profile"),
]

app_name = "items"