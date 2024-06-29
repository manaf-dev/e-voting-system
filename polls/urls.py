from django.urls import path

from .views import HomeView, BallotsView, VoteCompleteView
from . import views

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("<slug:election_slug>/ballots/", BallotsView.as_view(), name="ballots"),
    path(
        "vote/<int:election_id>/<int:candidate_id>/<int:position_id>/",
        views.vote,
        name="vote",
    ),
    path("voting/complete/", VoteCompleteView.as_view(), name="vote-complete"),
]
