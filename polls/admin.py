from django.contrib import admin
from .models import Election, Position, Candidate, Vote


# Register your models here.


@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    """Admin View for Candidate"""

    list_display = ("user", "election", "position")
    list_filter = ("election", "position")
    search_fields = ("user", "election", "position")


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    """Admin View for Vote"""

    list_display = ("candidate", "election", "position")
    list_filter = (
        "candidate",
        "election",
        "position",
    )
