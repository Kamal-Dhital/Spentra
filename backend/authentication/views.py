import random
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    RegisterSerializer,
    RequestPasswordResetSerializer,
    ResetPasswordSerializer,
)
from .models import CustomUser, PasswordResetOTP
from datetime import timedelta
from django.utils.timezone import now
import logging

logger = logging.getLogger(__name__)


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate a secure 6-digit OTP
            verification_code = str(random.randint(100000, 999999))
            user.verification_code = verification_code
            user.save()

            # Send the verification email
            send_mail(
                subject="Verify Your Spentra Account",
                message=f"""
Dear {user.full_name},

Thank you for signing up for Spentra! To complete your registration, please verify your email address by using the verification code below:

Verification Code: {verification_code}

If you did not sign up for Spentra, please ignore this email.

Best regards,
The Spentra Team
""",
                from_email="noreply@example.com",  # Use DEFAULT_FROM_EMAIL
                recipient_list=[user.email],
                fail_silently=False,
            )

            return Response(
                {"message": "User registered successfully! Verification email sent."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    def post(self, request):
        email = request.data.get("email")
        verification_code = request.data.get("verification_code")

        try:
            user = CustomUser.objects.get(email=email)
            if user.verification_code == verification_code:
                user.is_verified = True
                user.verification_code = None  # Clear the OTP after verification
                user.save()
                return Response(
                    {"message": "Email verified successfully!"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Invalid verification code."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        logger.info(f"Authenticating user with email: {email}")
        user = authenticate(email=email, password=password)

        if user:
            if user.is_verified:
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Email is not verified. Please verify your email."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        logger.error("Authentication failed. Invalid email or password.")
        return Response(
            {"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED
        )


class RequestPasswordResetView(APIView):
    def post(self, request):
        serializer = RequestPasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = CustomUser.objects.get(email=email)

            # Generate a secure 6-digit OTP
            otp = str(random.randint(100000, 999999))

            # Save OTP to the database
            PasswordResetOTP.objects.update_or_create(
                user=user,
                defaults={"otp": otp, "expires_at": now() + timedelta(minutes=10)},
            )

            # Send OTP to the user's email
            send_mail(
                subject="Password Reset Request",
                message=f"""
Dear {user.full_name},

You requested to reset your password. Use the OTP below to reset your password:

OTP: {otp}

This OTP will expire in 10 minutes. If you did not request this, please ignore this email.

Best regards,
The Spentra Team
""",
                from_email="noreply@example.com",
                recipient_list=[email],
                fail_silently=False,
            )

            return Response(
                {"message": "OTP sent to your email."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self, request):
        logger.info(f"Request data: {request.data}")  # Log the incoming request data
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Password reset successful."}, status=status.HTTP_200_OK
            )
        logger.error(f"Validation errors: {serializer.errors}")  # Log validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
