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


admin.site.register(Candidate)

admin.site.register(Vote)
