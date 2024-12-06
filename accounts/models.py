from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import date


# Create your models here.
class CustomUser(AbstractUser):
    middle_name = models.CharField(max_length=150, blank=True)
    level = models.CharField(max_length=5, default="100", blank=True)
    entry_date = models.DateField()
    phone = models.CharField(max_length=50, default="000")
    password_changed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        current_year = date.today().year
        entry_year = self.entry_date.year
        level = current_year - entry_year + 1
        self.level = str(level + "00")

        super(CustomUser, self).save(*args, **kwargs)

    def get_full_name(self):
        """
        Return the first_name plus middle_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.middle_name} {self.last_name}"
        return full_name.strip()

    def get_academic_years(self):
        academic_years = [self.entry_date.year + i for i in range(4)]

        print("model years", academic_years)
        return academic_years
