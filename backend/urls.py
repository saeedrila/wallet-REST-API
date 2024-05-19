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
from authentication.views import AccountSignup, AccountLogin, AccountLogout

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
    path("api/login", AccountLogin.as_view(), name="login"),
    path("api/logout", AccountLogout.as_view(), name="logout"),
]
