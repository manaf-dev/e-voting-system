from django.db import models
from accounts.models import CustomUser
from django.utils.text import slugify

from PIL import Image


# Create your models here.
class Election(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    slug = models.SlugField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Election, self).save(*args, **kwargs)  # Call the real save() method

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Candidate(models.Model):
    user = models.ForeignKey(
        CustomUser, verbose_name="Candidate", on_delete=models.CASCADE, default=1
    )
    election = models.ForeignKey(
        "Election", related_name="candidates", on_delete=models.CASCADE, default=1
    )
    position = models.ForeignKey(
        "Position", related_name="candidates", on_delete=models.CASCADE
    )
    profile_pic = models.ImageField(
        verbose_name="Profile Picture",
        default="profile.png",
        upload_to="Candidates_profiles",
    )

    def save(self, *args, **kwargs):
        img = Image.open(self.profile_pic.path)
        if img.height > 300 | img.width > 300:
            img.thumbnail((300, 300))
            img.save(self.profile_pic.path)
        super(Candidate, self).save(*args, **kwargs)  # Call the real save() method

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "election"],
                name="unique_candidate_position",
            )
        ]

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Vote(models.Model):
    voter = models.ForeignKey(
        CustomUser, related_name="voters", on_delete=models.CASCADE
    )
    candidate = models.ForeignKey(
        "Candidate", related_name="votes", on_delete=models.CASCADE
    )
    election = models.ForeignKey(
        "Election", related_name="votes", on_delete=models.CASCADE
    )
    position = models.ForeignKey(
        "Position", related_name="votes", on_delete=models.CASCADE, default=1
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        # unique_together = ('voter', 'position')
        constraints = [
            models.UniqueConstraint(
                fields=["voter", "election", "position"], name="unique_voter_position"
            )
        ]

    def __str__(self):
        return f"Vote for {self.election.name}"
