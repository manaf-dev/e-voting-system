from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages
from django.db.models import Count

from accounts.models import CustomUser
from .models import Election, Position, Candidate, Vote


# Create your views here.
class HomeView(LoginRequiredMixin, ListView):
    model = Election
    context_object_name = "elections"
    template_name = "polls/home.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Election.objects.filter(end_date__gt=timezone.now()).order_by("-id")
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


class BallotsView(LoginRequiredMixin, ListView):
    model = Position
    template_name = "polls/ballots.html"
    context_object_name = "positions"
    paginate_by = 1
    page_kwarg = "ballot"

    def get_queryset(self):
        election = get_object_or_404(Election, slug=self.kwargs["election_slug"])
        print(election)
        queryset = (
            Position.objects.filter(candidates__election=election)
            .distinct()
            .order_by("id")
        )

        # for i in queryset:
        #     print(i)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        election = get_object_or_404(Election, slug=self.kwargs["election_slug"])
        positions = self.get_queryset()

        context["election"] = election
        # context["positions"] = positions

        candidates_by_position = {
            position: Candidate.objects.filter(election=election, position=position)
            for position in positions
        }
        print(candidates_by_position)
        context["candidates_by_position"] = candidates_by_position
        return context


@login_required
def vote_candidate(request, election_slug, candidate_id, position_id):
    selected_candidates = request.session.get("selected_candidates", {})
    selected_candidates[str(position_id)] = candidate_id
    request.session["selected_candidates"] = selected_candidates
    print(request.session["selected_candidates"])

    next_page = request.GET.get("ballot")
    if not next_page:
        return redirect(
            "preview-votes",
            election_slug,
        )

    return redirect(
        reverse("ballots", kwargs={"election_slug": election_slug})
        + f"?ballot={next_page}"
    )
    # return redirect("home")


class PreviewVotesView(LoginRequiredMixin, TemplateView):
    template_name = "polls/preview_votes.html"

    def get_context_data(self, **kwargs):
        context = super(PreviewVotesView, self).get_context_data(**kwargs)
        election = get_object_or_404(Election, slug=self.kwargs["election_slug"])
        context["election"] = election

        selected_candidates = self.request.session.get("selected_candidates")
        context["selected_candidates"] = {
            position_id: Candidate.objects.get(id=candidate_id)
            for position_id, candidate_id in selected_candidates.items()
        }

        return context


@login_required
def submit_votes(request, election_slug):
    if request.method == "POST":
        election = get_object_or_404(Election, slug=election_slug)

        selected_candidates = request.session.get("selected_candidates")
        for position_id, candidate_id in selected_candidates.items():
            position = get_object_or_404(Position, id=position_id)
            candidate = get_object_or_404(Candidate, id=candidate_id)
            vote = Vote.objects.create(
                voter=request.user,
                candidate=candidate,
                election=election,
                position=position,
            )
        request.session["selected_candidates"] = {}
        messages.success(request, "You votes are submitted successfully!")
        return redirect("vote-complete", election_slug)

    return redirect("home")


class VoteCompleteView(LoginRequiredMixin, TemplateView):
    template_name = "polls/vote_complete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["election"] = get_object_or_404(
            Election, slug=self.kwargs["election_slug"]
        )
        return context


@login_required
def vote_results(request, election_slug):
    election = get_object_or_404(Election, slug=election_slug)
    if not election.results_published:
        messages.info(
            request, "Voting still in progress. Results are not yet published"
        )
        return redirect("home")
    positions = Position.objects.filter(candidates__election=election).distinct()

    results = []
    for position in positions:
        candidates = Candidate.objects.filter(
            election=election, position=position
        ).annotate(vote_count=Count("candidate"))
        total_votes = Vote.objects.filter(election=election, position=position).count()

        candidates_results = []
        for candidate in candidates:
            vote_count = candidate.vote_count
            vote_percentage = (vote_count / total_votes) * 100 if total_votes > 0 else 0

            candidates_results.append(
                {
                    "candidate": candidate,
                    "vote_count": vote_count,
                    "vote_percentage": vote_percentage,
                }
            )

        if candidates_results:
            winner = max(candidates_results, key=lambda x: x["vote_count"])
            winner["is_winner"] = True
        else:
            winner = None

        results.append(
            {
                "position": position,
                "candidates": candidates_results,
                "total_votes": total_votes,
                # "winner": winner,
            }
        )

    context = {"election": election, "results": results}
    return render(request, "polls/results.html", context)
