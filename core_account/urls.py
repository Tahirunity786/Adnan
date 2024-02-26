from django.urls import path
from core_account.views import (CreateUserView, GoogleAuthAPIView, GetNewOtp, VerifyOtp, SocialLoginView, UserLogin, UserSearchView)

urlpatterns = [
    # Endpoint for Google authentication
    path("public/auth/u/google", GoogleAuthAPIView.as_view(), name="new-user-google"),

    # Endpoint for user registration
    path("public/u/register", CreateUserView.as_view(), name="new-user"),

    # Endpoint for user login
    path("public/u/login", UserLogin.as_view(), name="user-login"),

    # Endpoint for generating a new OTP (One Time Password)
    path("public/u/auth/getnewotp", GetNewOtp.as_view(), name="account-otp"),

    # Endpoint for verifying OTP during user registration
    path("public/u/auth/verify", VerifyOtp.as_view(), name="new-user-verify"),

    # Endpoint for Facebook OAuth authentication
    path('public/oauth/facebook', SocialLoginView.as_view(), name="new-user-facebook"),

    # Endpoint for searching user accounts
    path('public/u/search/account', UserSearchView.as_view(), name='search-account'),
]
