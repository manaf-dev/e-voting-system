from django.urls import path

from .views import HomeView, PresidentBallotView
from . import views

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path(
        "<slug:slug>/ballots/", PresidentBallotView.as_view(), name="president-ballot"
    ),
    path("vote/<int:election_id>/<int:candidate_id>/", views.vote, name="vote"),
]
