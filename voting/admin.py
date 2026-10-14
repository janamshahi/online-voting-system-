
from django.contrib import admin
from django.db.models import Count
from django.shortcuts import render
from django.urls import path, reverse
from django.utils import timezone

from .models import (
    Ballot,
    Candidate,
    Election,
    Participation,
    VoterProfile,
)


# =========================================================
# ELECTION ADMIN
# =========================================================

@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "opens_at",
        "closes_at",
        "is_published",
        "results_published",
        "candidate_total",
        "participation_total",
    )

    list_filter = (
        "is_published",
        "results_published",
        "opens_at",
    )

    search_fields = ("title", "description")

    list_editable = (
        "is_published",
        "results_published",
    )

    date_hierarchy = "opens_at"
    ordering = ("-opens_at",)

    @admin.display(description="Candidates")
    def candidate_total(self, obj):
        return obj.candidates.count()

    @admin.display(description="Participation")
    def participation_total(self, obj):
        return obj.participations.count()


# =========================================================
# CANDIDATE ADMIN
# =========================================================

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "position",
        "election",
        "is_active",
    )

    list_filter = (
        "is_active",
        "election",
        "position",
    )

    search_fields = (
        "full_name",
        "position",
        "election__title",
    )

    list_editable = ("is_active",)
    list_select_related = ("election",)


# =========================================================
# VOTER PROFILE ADMIN
# =========================================================

@admin.register(VoterProfile)
class VoterProfileAdmin(admin.ModelAdmin):
    list_display = (
        "student_id",
        "user",
        "is_eligible",
    )

    list_filter = ("is_eligible",)

    search_fields = (
        "student_id",
        "user__username",
        "user__first_name",
        "user__last_name",
    )

    list_editable = ("is_eligible",)
    list_select_related = ("user",)


# =========================================================
# PARTICIPATION ADMIN
# =========================================================

@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = (
        "election",
        "voter",
        "cast_at",
    )

    list_filter = (
        "election",
        "cast_at",
    )

    search_fields = (
        "election__title",
        "voter__username",
    )

    date_hierarchy = "cast_at"
    list_select_related = ("election", "voter")

    readonly_fields = (
        "election",
        "voter",
        "cast_at",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# =========================================================
# BALLOT ADMIN
# =========================================================

@admin.register(Ballot)
class BallotAdmin(admin.ModelAdmin):
    list_display = (
        "election",
        "candidate",
        "cast_at",
    )

    list_filter = (
        "election",
        "cast_at",
    )

    search_fields = (
        "election__title",
        "candidate__full_name",
    )

    date_hierarchy = "cast_at"

    list_select_related = (
        "election",
        "candidate",
    )

    readonly_fields = (
        "election",
        "candidate",
        "cast_at",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# =========================================================
# VOTING RESULTS VIEW
# =========================================================

def voting_results_view(request):
    """
    Display aggregate election results inside Django/Jazzmin admin.
    """

    now = timezone.now()

    elections = Election.objects.annotate(
        total_votes=Count("ballots", distinct=True),
        total_participants=Count(
            "participations",
            distinct=True,
        ),
        total_candidates=Count(
            "candidates",
            distinct=True,
        ),
    ).order_by("-opens_at")

    election_results = []

    for election in elections:

        candidates = Candidate.objects.filter(
            election=election,
            is_active=True,
        ).annotate(
            vote_count=Count("ballots", distinct=True),
        ).order_by("-vote_count", "full_name")

        total_votes = election.total_votes

        candidate_results = []

        for candidate in candidates:
            percentage = (
                round(candidate.vote_count * 100 / total_votes, 1)
                if total_votes > 0
                else 0
            )

            candidate_results.append({
                "candidate": candidate,
                "vote_count": candidate.vote_count,
                "percentage": percentage,
            })

        if not election.is_published:
            status = "Unpublished"
        elif now < election.opens_at:
            status = "Upcoming"
        elif now <= election.closes_at:
            status = "Voting Open"
        else:
            status = "Closed"

        election_results.append({
            "election": election,
            "total_votes": total_votes,
            "total_participants": election.total_participants,
            "total_candidates": election.total_candidates,
            "candidate_results": candidate_results,
            "status": status,
            "results_published": election.results_published,
        })

    context = {
        **admin.site.each_context(request),
        "title": "Voting Results",
        "election_results": election_results,
        "total_elections": elections.count(),
        "total_votes_all": sum(
            election.total_votes for election in elections
        ),
        "total_participants_all": sum(
            election.total_participants for election in elections
        ),
    }

    return render(
        request,
        "admin/voting_results.html",
        context,
    )


# =========================================================
# REGISTER CUSTOM RESULTS URL IN THE EXISTING ADMIN SITE
# =========================================================

_original_admin_get_urls = admin.site.get_urls


def _admin_get_urls_with_results():
    custom_urls = [
        path(
            "voting-results/",
            admin.site.admin_view(voting_results_view),
            name="voting_results",
        ),
    ]

    return custom_urls + _original_admin_get_urls()


admin.site.get_urls = _admin_get_urls_with_results
