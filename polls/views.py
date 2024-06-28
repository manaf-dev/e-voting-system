from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
from django.utils import timezone

from accounts.models import CustomUser
from .models import Election, Position, Candidate, Vote


# Create your views here.
class HomeView(ListView):
    model = Election
    context_object_name = "elections"
    template_name = "polls/home.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Election.objects.filter(end_date__gt=timezone.now())
        return queryset


class PresidentBallotView(ListView):
    model = Candidate
    context_object_name = "presidents"
    template_name = "polls/president_ballot.html"

    def get_queryset(self):
        self.election = Election.objects.get(slug=self.kwargs["slug"])
        self.position = Position.objects.get(name="President")
        queryset = Candidate.objects.filter(
            election=self.election, position=self.position
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["election"] = self.election
        context["position"] = self.position
        return context


def vote(request, election_id, candidate_id):
    if request.method == "POST":
        # user = CustomUser.objects.get(id=candidate_id)
        candidate = get_object_or_404(Candidate, id=candidate_id)
        election = get_object_or_404(Election, id=election_id)
        vote = Vote.objects.create(
            voter=request.user, candidate=candidate, election=election
        )
        return redirect("home")
    return redirect("home")
