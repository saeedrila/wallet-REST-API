from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Wallet
from authentication.models import CustomUser

"""
Signals are used to automatically create wallet when a user is created.
"""


@receiver(post_save, sender=CustomUser)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_wallet(sender, instance, **kwargs):
    instance.wallet.save()
