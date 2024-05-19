from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from .models import Wallet, Transaction
from .serializers import (
    WalletSerializer,
    TransactionSerializer,
    TransactionHistorySerializer,
)


class WalletBalance(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet = Wallet.objects.get(user=request.user)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)


class WalletDeposit(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get("amount")
        wallet = Wallet.objects.get(user=request.user)
        transaction = Transaction.objects.create(
            user=request.user, amount=amount, transaction_type=Transaction.DEPOSIT
        )

        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)


class WalletWithdrawal(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get("amount")
        wallet = Wallet.objects.get(user=request.user)
        if wallet.balance < amount:
            return Response(
                {"error": "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST
            )

        transaction = Transaction.objects.create(
            user=request.user, amount=amount, transaction_type=Transaction.WITHDRAWAL
        )
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)


class TransactionHistory(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user)
        serializer = TransactionHistorySerializer(transactions, many=True)
        return Response(serializer.data)
