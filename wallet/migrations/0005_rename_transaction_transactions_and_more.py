# Generated by Django 5.0.6 on 2024-05-19 14:04

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("wallet", "0004_alter_transaction_amount"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Transaction",
            new_name="Transactions",
        ),
        migrations.RenameIndex(
            model_name="transactions",
            new_name="wallet_tran_user_id_97baf4_idx",
            old_name="wallet_tran_user_id_b00b9e_idx",
        ),
    ]
