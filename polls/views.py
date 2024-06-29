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
        current_page = int(request.POST.get("ballot", 1))
        next_page = current_page + 1
        return redirect(
            reverse("ballots", kwargs={"election_slug": election.slug})
            + f"?ballot={next_page}"
        )
    return redirect("home")


class VoteCompleteView(TemplateView):
    template_name = "vote_complete.html"
