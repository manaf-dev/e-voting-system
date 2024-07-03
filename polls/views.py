from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, TemplateView
from django.utils import timezone
from django.urls import reverse

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        elections = self.get_queryset()
        elections_status = [
            {
                "election": election,
                "status": has_user_finished_voting(self.request.user.id, election.id),
            }
            for election in elections
        ]
        context["elections_status"] = elections_status
        return context


def has_user_finished_voting(user, election):
    positions = (
        Position.objects.filter(candidates__election=election).distinct().count()
    )
    user_votes = Vote.objects.filter(voter=user, election=election).count()
    if not positions or not user_votes:
        return False
    return positions == user_votes


class BallotsView(ListView):
    model = Position
    context_object_name = "candidates"
    template_name = "polls/ballots.html"
    paginate_by = 1
    page_kwarg = "ballot"

    # def get_queryset(self):
    #     self.election = Election.objects.get(slug=self.kwargs["slug"])
    #     queryset = Position.objects.
    #     return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        election = Election.objects.get(slug=self.kwargs["election_slug"])
        context["election"] = election
        # context["position"] = self.position
        return context


def vote(request, election_id, candidate_id, position_id):
    if request.method == "POST":
        # user = CustomUser.objects.get(id=candidate_id)
        candidate = get_object_or_404(Candidate, id=candidate_id)
        election = get_object_or_404(Election, id=election_id)
        position = get_object_or_404(Position, id=position_id)
        vote = Vote.objects.create(
            voter=request.user,
            candidate=candidate,
            election=election,
            position=position,
        )
        next_page = request.POST.get("ballot")
        if not next_page:
            return redirect("vote-complete")

        return redirect(
            reverse("ballots", kwargs={"election_slug": election.slug})
            + f"?ballot={next_page}"
        )
    return redirect("home")


class VoteCompleteView(TemplateView):
    template_name = "polls/vote_complete.html"
