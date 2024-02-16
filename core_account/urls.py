from django.urls import path
from core_account.views import (CreateUserView, GoogleAuthAPIView, GetNewOtp, VerifyOtp, SocialLoginView)


urlpatterns = [
    path("public/auth/u/google", GoogleAuthAPIView.as_view(), name="new-user-google"),
    path("public/u/register", CreateUserView.as_view(), name="new-user"),
    path("public/u/auth/getnewotp", GetNewOtp.as_view(), name="account-otp"),
    path("public/u/auth/verify", VerifyOtp.as_view(), name="new-user-verify"),
    path('public/oauth/facebook', SocialLoginView.as_view(), name="new-user-facebook"),
 
]
