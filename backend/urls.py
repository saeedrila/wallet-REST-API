# Importing from django
from django.contrib import admin
from django.urls import path

# Importing from DRF
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
    TokenVerifyView,
)

# Custom imports
from authentication.views import (
    AccountSignup,
    AccountSignupAdmin,
    AccountLogin,
    AccountLogout,
    UserListView,
    TransactionHistoryUser,
)
from wallet.views import (
    WalletBalance,
    WalletDeposit,
    WalletWithdrawal,
    TransactionHistory,
)

urlpatterns = [
    # Admin page
    path("admin/", admin.site.urls),
    # JWT Refresh and access tokens
    path(
        "token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),  # for obtaining access tokens
    path(
        "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # for refreshing tokens
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    # Login, Signup, Logout
    path("api/signup", AccountSignup.as_view(), name="signup"),
    path("api/signup-admin", AccountSignupAdmin.as_view(), name="signup-admin"),
    path("api/login", AccountLogin.as_view(), name="login"),
    path("api/logout", AccountLogout.as_view(), name="logout"),
    # List all users
    path("api/list-users", UserListView.as_view(), name="list-users"),
    path("wallet/balance/", WalletBalance.as_view(), name="wallet-balance"),
    path("wallet/deposit/", WalletDeposit.as_view(), name="wallet-deposit"),
    path("wallet/withdraw/", WalletWithdrawal.as_view(), name="wallet-withdrawal"),
    path(
        "wallet/transaction-history/",
        TransactionHistory.as_view(),
        name="transaction-history",
    ),
    path(
        "wallet/transaction-history/user/",
        TransactionHistoryUser.as_view(),
        name="transaction-history-user",
    ),
]
