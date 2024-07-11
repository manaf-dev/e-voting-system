from django.urls import path

from .views import HomeView, BallotsView, VoteCompleteView, PreviewVotesView
from . import views

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("<slug:election_slug>/ballots/", BallotsView.as_view(), name="ballots"),
    path(
        "vote/<slug:election_slug>/<int:position_id>/<int:candidate_id>/",
        views.vote_candidate,
        name="vote-candidate",
    ),
    path(
        "<slug:election_slug>/preview/",
        PreviewVotesView.as_view(),
        name="preview-votes",
    ),
    path(
        "submit_votes/<slug:election_slug>/",
        views.submit_votes,
        name="submit-votes",
    ),
    path(
        "<slug:election_slug>/complete/",
        VoteCompleteView.as_view(),
        name="vote-complete",
    ),
]
