from django.db import models
from django.conf import settings
from authentication.models import CustomUser


class Wallet(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="wallet"
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}'s wallet"


class Transaction(models.Model):
    WITHDRAWAL = "withdrawal"
    DEPOSIT = "deposit"
    TRANSACTION_CHOICES = [
        (WITHDRAWAL, "Withdrawal"),
        (DEPOSIT, "Deposit"),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
        ]
