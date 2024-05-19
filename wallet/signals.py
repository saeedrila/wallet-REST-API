from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Wallet, Transaction
from authentication.models import CustomUser


@receiver(post_save, sender=CustomUser)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_wallet(sender, instance, **kwargs):
    instance.wallet.save()


@receiver(post_save, sender=Transaction)
def update_wallet_balance(sender, instance, created, **kwargs):
    if created:
        wallet = Wallet.objects.get(user=instance.user)

        amount = Decimal(instance.amount)

        if instance.transaction_type == "withdrawal":
            wallet.balance -= amount
        elif instance.transaction_type == "deposit":
            wallet.balance += amount

        wallet.save()
