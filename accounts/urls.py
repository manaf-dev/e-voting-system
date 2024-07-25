from django.urls import path
from .views import CustomPasswordChangeView
from . import views


urlpatterns = [
    path(
        "change_password/", CustomPasswordChangeView.as_view(), name="change_password"
    ),
    path("add-new-voters/", views.add_new_voters, name="add-voters"),
    # path("logout/", views.logout, name="logout"),
]
