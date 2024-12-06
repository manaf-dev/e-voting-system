from django.db import models

from accounts.models import CustomUser


class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    paystack_ref = models.CharField(max_length=15, blank=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"Payment {self.id}"


class DuesRegister(models.Model):
    member = models.ForeignKey(
        CustomUser, related_name="dues", on_delete=models.CASCADE
    )
    academic_year = models.CharField(max_length=50)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.member.username} {self.academic_year}"


class Donation(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50)

    def __str__(self):
        return f"Donation from {self.phone}"
