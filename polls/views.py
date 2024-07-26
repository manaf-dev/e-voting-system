from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages
from django.db.models import Count
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from accounts.models import CustomUser
from .models import Election, Position, Candidate, Vote, VoteToken
import logging
import io

# logger = logging.getLogger(__name__)


# Create your views here.


@login_required
def index(request):
    return redirect("home")


class HomeView(LoginRequiredMixin, ListView):
    model = Election
    context_object_name = "elections"
    template_name = "polls/home.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Election.objects.filter(is_active=True).order_by("-id")
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
    try:
        token = VoteToken.objects.get(voter=user, election=election)
    except Exception:
        return False
    user_votes = Vote.objects.filter(token=token, election=election).count()
    if not positions or not user_votes:
        return False
    return positions == user_votes


def start_voting(request, election_slug):
    election = get_object_or_404(Election, slug=election_slug)
    start_time = election.start_date.strftime("%I:%M %p")
    start_date = election.start_date.strftime("%A, %x")
    if election.start_date > timezone.now():
        messages.info(
            request,
            f"Sorry! {election.name} is scheduled to start at {start_time} on {start_date}, see you then.",
        )
        return redirect("home")
    elif election.end_date < timezone.now():
        messages.info(
            request,
            f"Voting for {election.name} has endend. This is the results.",
        )
        return redirect("vote-results", election.slug)

    try:
        token = VoteToken.objects.get(voter=request.user, election=election)
        print(token.token)
        return redirect("ballots", election.slug)
    except Exception:
        token = VoteToken.objects.create(voter=request.user, election=election)
        print(token.token)
        return redirect("ballots", election.slug)


class BallotsView(LoginRequiredMixin, ListView):
    model = Position
    template_name = "polls/ballots.html"
    context_object_name = "positions"
    paginate_by = 1
    page_kwarg = "ballot"

    def get_queryset(self):
        election = get_object_or_404(Election, slug=self.kwargs["election_slug"])
        queryset = (
            Position.objects.filter(candidates__election=election)
            .distinct()
            .order_by("id")
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        election = get_object_or_404(Election, slug=self.kwargs["election_slug"])
        positions = self.get_queryset()

        context["election"] = election

        candidates_by_position = {
            position: Candidate.objects.filter(election=election, position=position)
            for position in positions
        }
        context["candidates_by_position"] = candidates_by_position
        return context


@login_required
def vote_candidate(request, election_slug, candidate_id, position_id):
    selected_candidates = request.session.get("selected_candidates", {})
    selected_candidates[str(position_id)] = candidate_id
    request.session["selected_candidates"] = selected_candidates
    # print(request.session["selected_candidates"])

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


def vote_candidate_no(request, election_slug, ballot, position_id):
    if ballot:
        selected_candidates = request.session.get("selected_candidates", {})
        selected_candidates[str(position_id)] = "NULL"
        request.session["selected_candidates"] = selected_candidates

        if ballot == 100:
            return redirect(
                "preview-votes",
                election_slug,
            )
        return redirect(
            reverse("ballots", kwargs={"election_slug": election_slug})
            + f"?ballot={ballot}"
        )
    return redirect(request.path)


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
            if candidate_id != "NULL"
        }

        return context


@login_required
def submit_votes(request, election_slug):
    if request.method == "POST":
        election = get_object_or_404(Election, slug=election_slug)

        selected_candidates = request.session.get("selected_candidates")
        for position_id, candidate_id in selected_candidates.items():
            position = get_object_or_404(Position, id=position_id)
            candidate = (
                "NULL"
                if candidate_id == "NULL"
                else get_object_or_404(Candidate, id=candidate_id)
            )
            token = VoteToken.objects.get(voter=request.user, election=election)

            if candidate == "NULL":
                vote = Vote.objects.create(
                    token=token,
                    election=election,
                    position=position,
                )
            else:
                vote = Vote.objects.create(
                    token=token,
                    candidate=candidate,
                    election=election,
                    position=position,
                )

        # logger.info(f"{request.user.first_name} has voted in {election.name}.")

        request.session["selected_candidates"] = {}
        messages.success(request, "Your votes are submitted successfully!")
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
        ).annotate(vote_count=Count("votes"))
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
            max_vote_count = max(count["vote_count"] for count in candidates_results)
            winners = [
                result
                for result in candidates_results
                if result["vote_count"] == max_vote_count
            ]

            if len(winners) > 1:
                for candidate in candidates_results:
                    candidate["is_tie"] = candidate in winners
                    candidate["is_winner"] = False
            else:
                for candidate in candidates_results:
                    candidate["is_tie"] = False
                    candidate["is_winner"] = candidate in winners

        # print(candidates_results)

        results.append(
            {
                "position": position,
                "candidates": candidates_results,
                "total_votes": total_votes,
            }
        )
    total_voters = CustomUser.objects.all().count()
    total_turn_out = Vote.objects.filter(election=election).count()
    context = {
        "election": election,
        "results": results,
        "total_voters": total_voters,
        "total_turn_out": total_turn_out,
    }
    return render(request, "polls/results.html", context)


@staff_member_required
def read_logs(request):
    filename = settings.BASE_DIR / "info.log"
    with open(filename, "r") as log_file:
        log_content = log_file.read()
    context = {"log_content": log_content}
    return render(request, "logs.html", context)


@staff_member_required
def print_results(request, election_slug):
    election = get_object_or_404(Election, slug=election_slug)
    positions = Position.objects.filter(candidates__election=election).distinct()

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, letter)
    p.setFont("Helvetica", 12)

    width, height = letter

    y = height - 40
    p.drawString(
        100,
        y,
        f"Results for {election.name}",
    )
    y -= 30

    for position in positions:
        candidates = position.candidates.filter(election=election)
        p.drawString(100, y, f"Position: {position.name}")
        y -= 20

        for candidate in candidates:
            vote_count = Vote.objects.filter(
                election=election, position=position, candidate=candidate
            ).count()
            p.drawString(
                120, y, f"{candidate.user.get_full_name()}: {vote_count} votes"
            )
            y -= 20

        y -= 20  # Add extra space between positions

    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="election_results.pdf")
