# Generated by Django 5.0.6 on 2024-07-14 00:09

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0008_alter_vote_candidate_alter_vote_election_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="VoteToken",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("token", models.UUIDField(default=uuid.uuid4, unique=True)),
            ],
        ),
        migrations.RemoveConstraint(
            model_name="vote",
            name="unique_voter_position",
        ),
        migrations.RemoveField(
            model_name="vote",
            name="voter",
        ),
        migrations.AlterField(
            model_name="vote",
            name="candidate",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="votes",
                to="polls.candidate",
            ),
        ),
        migrations.AlterField(
            model_name="vote",
            name="election",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="votes",
                to="polls.election",
            ),
        ),
        migrations.AlterField(
            model_name="vote",
            name="position",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="votes",
                to="polls.position",
            ),
        ),
        migrations.AddField(
            model_name="votetoken",
            name="election",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="polls.election"
            ),
        ),
        migrations.AddField(
            model_name="votetoken",
            name="voter",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="vote",
            name="token",
            field=models.ForeignKey(
                default=101,
                on_delete=django.db.models.deletion.CASCADE,
                to="polls.votetoken",
            ),
        ),
        migrations.AddConstraint(
            model_name="vote",
            constraint=models.UniqueConstraint(
                fields=("token", "election", "position"), name="unique_voter_position"
            ),
        ),
    ]