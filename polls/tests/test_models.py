from django.test import TestCase
from django.utils import timezone
from django.db import IntegrityError

from polls.models import Election, Position, Candidate, Vote
from accounts.models import CustomUser


class ElectionModelTests(TestCase):
    def setUp(self):
        self.election = Election.objects.create(
            name="Test Election",
            description="Test election description",
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=1),
        )

    def test_election_creation(self):
        self.assertEqual(self.election.name, "Test Election")
        self.assertIsInstance(self.election.start_date, timezone.datetime)


class PositionModelTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Test Position")

    def test_position_creation(self):
        self.assertTrue(self.position.name, "Test Position")


class CandidateModelTests(TestCase):

    # @classmethod
    def SetUp(self):
        self.user1 = CustomUser.objects.create_user(
            username="TestUser1",
            password="testpass123",
        )
        self.user2 = CustomUser.objects.create_user(
            username="TestUser2",
            password="testpass123",
        )

        self.election = Election.objects.create(
            name="Test Election",
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=1),
        )

        self.position = Position.objects.create(name="Test Position")
        # cls.position = Position.objects.create(name="Test Position")

        # def setUp(self):
        self.candidate = Candidate.objects.create(
            user=self.user1,
            election=self.election,
            position=self.position,
        )

    def test_candidate_creation(self):
        self.assertTrue(self.election.name, "Test Election")
        self.assertTrue(self.position.name, "Test Position")
        self.assertTrue(self.candidate.user.username, "TestUser1")

    def test_unique_candidate_in_election(self):
        with self.assertRaises(IntegrityError):
            Candidate.objects.create(
                user=self.user1,
                election=self.election,
                position=self.position,
            )

        # candidate2 = Candidate.objects.create(
        #     user=self.testuser2,
        #     election=self.election,
        #     position=self.position
        # )
