from rest_framework import serializers

from .models import Wallet, Transaction


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["balance", "created_at", "updated_at"]


class TransactionSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    wallet_balance = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ["amount", "transaction_type", "timestamp", "wallet_balance"]

    def get_wallet_balance(self, obj):
        wallet_balance = obj.user.wallet.balance
        return wallet_balance


class TransactionHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ["amount", "transaction_type", "timestamp"]
