from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models
from datetime import timedelta
from django.utils.timezone import now


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)  # Email verification flag
    verification_code = models.CharField(max_length=6, blank=True, null=True)  # OTP

    username = None  # Remove the username field

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # Avoid conflict with default User.groups
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",  # Avoid conflict with default User.user_permissions
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email


def default_expiration_time():
    """Returns the default expiration time for OTPs (10 minutes from now)."""
    return now() + timedelta(minutes=10)


class PasswordResetOTP(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="password_reset_otp"
    )
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(
        default=default_expiration_time
    )  # Use function instead of lambda

    def is_valid(self):
        """Check if the OTP is still valid."""
        return now() < self.expires_at
