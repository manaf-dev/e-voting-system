from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html

from .models import Election, Position, Candidate, Vote
from .views import read_logs


class ElectionAdminSite(admin.AdminSite):
    site_header = "GMSA Election HQ"

    def get_urls(self):
        urls = super().get_urls()
        custom_url = [
            path("read_logs/", self.admin_view(read_logs), name="read_logs"),
        ]
        return urls + custom_url


# custom_admin_site = ElectionAdminSite()


@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date", "view_results")
    prepopulated_fields = {"slug": ("name",)}

    def view_results(self, obj):
        return format_html(
            '<a href="{}">View Results</a>', reverse("vote-results", args=[obj.slug])
        )

    # def read_logs(self, obj):
    #     return format_html('<a href="{}">Read Logs</a>', reverse("read_logs"))


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

    list_display = ("election", "position")
    list_filter = ("election", "position")
    fields = ["election", "position"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            return False
        return False

    def has_delete_permission(self, request, obj=None):
        return False
