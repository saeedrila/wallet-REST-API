from django.core.management import BaseCommand
from wallet.models import Transaction
from authentication.models import CustomUser
import random


class Command(BaseCommand):
    """
    This is used to create some sample transactions to all users.
    """

    help = "This adds new transations to all users."

    def handle(self, *args, **kwargs):
        users = CustomUser.objects.all()

        for user in users:
            Transaction.objects.create(
                user=user,
                amount=100.00,
                transaction_type=Transaction.DEPOSIT,
            )
            random_debit_amount = random.randint(1, 100)
            Transaction.objects.create(
                user=user,
                amount=random_debit_amount,
                transaction_type=Transaction.WITHDRAWAL,
            )

        self.stdout.write(
            self.style.SUCCESS("Successfully updated transaction table for all users")
        )
