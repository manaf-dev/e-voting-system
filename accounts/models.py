from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    middle_name = models.CharField(max_length=150, blank=True)
    password_changed = models.BooleanField(default=False)
    level = models.CharField(max_length=5, default="100")

    def get_full_name(self):
        """
        Return the first_name plus middle_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.middle_name} {self.last_name}"
        return full_name.strip()
