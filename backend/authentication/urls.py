from django.urls import path
from .views import (
    RegisterView,
    VerifyEmailView,
    LoginView,
    RequestPasswordResetView,
    ResetPasswordView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("login/", LoginView.as_view(), name="login"),
    path(
        "forgot-password/", RequestPasswordResetView.as_view(), name="forgot-password"
    ),
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
]
