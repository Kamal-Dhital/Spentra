from django.urls import path
from .views import (
    RegistrationView,
    LoginView,
    PasswordResetRequestView,
    PasswordResetView,
)

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path(
        "password-reset-request/",
        PasswordResetRequestView.as_view(),
        name="password-reset-request",
    ),
    path("password-reset/", PasswordResetView.as_view(), name="password-reset"),
]
