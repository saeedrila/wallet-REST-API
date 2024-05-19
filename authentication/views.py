# Importing modules from django
from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, login, logout
from django.db import transaction

# Importing modules from DRF
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated

# Importing from this django project
from .serializers import AccountSerializer, LoginSerializer, UserSerializer
from .models import CustomUser
from wallet.models import Transactions
from wallet.serializers import TransactionHistorySerializer

"""
Account Signup and Account signup for admin are created separately and can be
accessed from seperate urls.
"""


# Account signup
class AccountSignup(APIView):
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Admin Account signup
class AccountSignupAdmin(APIView):
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_staff = True
            user.is_superuser = True
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Account Login
class AccountLogin(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                access_token = RefreshToken.for_user(user)
                refresh_token = RefreshToken.for_user(user)

                return Response(
                    {
                        "message": "Login successful",
                        "accessToken": str(access_token.access_token),
                        "refreshToken": str(refresh_token),
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Account Logout
class AccountLogout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "User is not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


"""
UserListView and TransactionHistoryUser provides list of all users and transactions of
a provided user ID. These two views can be accesses by staff or admin user only.
Admin users has to be created using "api/signup-admin" url.
"""


# List all users
class UserListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Lists all transactions of user with given user ID
class TransactionHistoryUser(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        user_id = request.query_params.get("user_id")
        if user_id is not None:
            transactions = Transactions.objects.filter(user_id=user_id)
            print(transactions)
            serializer = TransactionHistorySerializer(transactions, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "user_id query parameter is required"}, status=400
            )
