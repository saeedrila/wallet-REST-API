from django.db import transaction
from decimal import Decimal

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Wallet, Transactions
from .serializers import (
    WalletSerializer,
    TransactionSerializer,
    TransactionHistorySerializer,
)

"""
The views in wallet app contains views to be used by all users. It fetches wallet balance,
Deposits amount by creating transaction in the transaction table,
Withdraws amount by creating transaciton in the transaction table.
It also have view for showing transaction of the user.

Both Deposit and Withdraw is carried out with atomic transactions. 
A recorded and the balance in the wallet table is updated as a transaction.
"""


class WalletBalance(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet = Wallet.objects.get(user=request.user)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)


class WalletDeposit(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        amount = request.data.get("amount")
        wallet = Wallet.objects.get(user=request.user)

        try:
            transaction = Transactions.objects.create(
                user=request.user, amount=amount, transaction_type=Transactions.DEPOSIT
            )

            if transaction.transaction_type == "deposit":
                wallet.balance += Decimal(amount)
                wallet.save()

            serializer = TransactionSerializer(transaction)
            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"error": f"Failed to create transaction: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class WalletWithdrawal(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        amount = request.data.get("amount")
        wallet = Wallet.objects.get(user=request.user)

        if wallet.balance < amount:
            return Response(
                {"error": "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            transaction = Transactions.objects.create(
                user=request.user,
                amount=amount,
                transaction_type=Transactions.WITHDRAWAL,
            )
            wallet.balance -= Decimal(amount)
            wallet.save()
            serializer = TransactionSerializer(transaction)
            return Response(serializer.data)

        except Exception as e:
            transaction.rollback()
            return Response(
                {"error": f"Failed to create transaction: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TransactionHistory(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transactions.objects.filter(user=request.user)
        serializer = TransactionHistorySerializer(transactions, many=True)
        return Response(serializer.data)
