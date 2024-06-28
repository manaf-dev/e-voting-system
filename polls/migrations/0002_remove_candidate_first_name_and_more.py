# Generated by Django 5.0.6 on 2024-06-26 13:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="candidate",
            name="first_name",
        ),
        migrations.RemoveField(
            model_name="candidate",
            name="last_name",
        ),
        migrations.RemoveField(
            model_name="candidate",
            name="middle_name",
        ),
        migrations.RemoveField(
            model_name="position",
            name="election",
        ),
        migrations.AddField(
            model_name="candidate",
            name="election",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="candidates",
                to="polls.election",
            ),
        ),
        migrations.AddField(
            model_name="candidate",
            name="user",
            field=models.OneToOneField(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="candidate",
            ),
        ),
        migrations.AddConstraint(
            model_name="vote",
            constraint=models.UniqueConstraint(
                fields=("voter", "candidate", "election"), name="unique_voter_position"
            ),
        ),
    ]