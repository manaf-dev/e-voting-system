from django.test import TestCase

from accounts.models import CustomUser


class AccountTests(TestCase):
    def test_user_creation(self):
        user = CustomUser.objects.create_user(
            username="testUser", password="testpass123"
        )
        self.assertEqual(user.username, "testUser")
