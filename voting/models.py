
from django.conf import settings
from django.db import models, transaction
from django.utils import timezone


class VoterProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="voter_profile"
    )

    student_id = models.CharField(
        max_length=40,
        unique=True,
        blank=True
    )

    is_eligible = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Generate a Student ID automatically for new voter profiles.
        if not self.student_id:
            prefix = "WCA2026"

            with transaction.atomic():
                last_profile = (
                    VoterProfile.objects
                    .select_for_update()
                    .filter(student_id__startswith=prefix)
                    .order_by("-student_id")
                    .first()
                )

                if last_profile:
                    try:
                        last_number = int(
                            last_profile.student_id[len(prefix):]
                        )
                    except ValueError:
                        last_number = 0
                    next_number = last_number + 1
                else:
                    next_number = 1

                self.student_id = f"{prefix}{next_number:03d}"

                # Avoid overwriting explicitly selected update fields.
                if kwargs.get("update_fields") is not None:
                    kwargs["update_fields"] = set(kwargs["update_fields"]) | {
                        "student_id"
                    }

                super().save(*args, **kwargs)
                return

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student_id} — {self.user.get_username()}"


class Election(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    opens_at = models.DateTimeField()
    closes_at = models.DateTimeField()
    is_published = models.BooleanField(default=False)
    results_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-opens_at"]

    def __str__(self):
        return self.title

    @property
    def is_open(self):
        now = timezone.now()
        return (
            self.is_published
            and self.opens_at <= now <= self.closes_at
        )


class Candidate(models.Model):
    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE,
        related_name="candidates"
    )
    full_name = models.CharField(max_length=120)
    position = models.CharField(
        max_length=100,
        default="Student Representative"
    )
    manifesto = models.TextField(blank=True)
    photo = models.ImageField(
        upload_to="candidate_photos/",
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["full_name"]
        constraints = [
            models.UniqueConstraint(
                fields=["election", "full_name"],
                name="unique_candidate_per_election"
            )
        ]

    def __str__(self):
        return f"{self.full_name} — {self.election.title}"


class Participation(models.Model):
    """
    Records that a voter has participated without storing their
    candidate choice in the participation record.
    """
    election = models.ForeignKey(
        Election,
        on_delete=models.PROTECT,
        related_name="participations"
    )
    voter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="participations"
    )
    cast_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["election", "voter"],
                name="one_participation_per_voter_election"
            )
        ]

    def __str__(self):
        return (
            f"{self.voter.get_username()} "
            f"participated in {self.election}"
        )


class Ballot(models.Model):
    """
    Stores a candidate choice separately from the participation record.
    """
    election = models.ForeignKey(
        Election,
        on_delete=models.PROTECT,
        related_name="ballots"
    )
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.PROTECT,
        related_name="ballots"
    )
    cast_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ballot for {self.election.title}"
