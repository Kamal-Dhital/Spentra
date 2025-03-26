from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from .serializers import (
    RegistrationSerializer,
    LoginSerializer,
    PasswordResetRequestSerializer,
    PasswordResetSerializer,
)
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

User = get_user_model()


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "User registered successfully. Check your email for verification."
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
            )
            if user:
                if not user.is_email_verified:
                    return Response(
                        {"error": "Email not verified."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                update_last_login(None, user)
                return Response(
                    {"message": "Login successful."}, status=status.HTTP_200_OK
                )
            return Response(
                {"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(email=serializer.validated_data["email"]).first()
            if user:
                otp = get_random_string(length=6, allowed_chars="0123456789")
                user.otp = otp
                user.save()
                send_mail(
                    "Password Reset OTP",
                    f"Your OTP is {otp}",
                    "noreply@example.com",
                    [user.email],
                )
            return Response(
                {"message": "If the email exists, an OTP has been sent."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(
                email=serializer.validated_data["email"],
                otp=serializer.validated_data["otp"],
            ).first()
            if user:
                if (
                    serializer.validated_data["new_password"]
                    != serializer.validated_data["confirm_password"]
                ):
                    return Response(
                        {"error": "Passwords do not match."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                user.set_password(serializer.validated_data["new_password"])
                user.otp = None
                user.save()
                return Response(
                    {"message": "Password reset successful."}, status=status.HTTP_200_OK
                )
            return Response(
                {"error": "Invalid OTP or email."}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
