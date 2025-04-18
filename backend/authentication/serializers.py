from rest_framework import serializers
from .models import CustomUser, PasswordResetOTP


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["full_name", "email", "password", "confirm_password"]

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")  # Remove confirm_password before saving
        user = CustomUser.objects.create_user(**validated_data)  # Hashes password
        return user


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user is associated with this email.")
        return value


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        try:
            user = CustomUser.objects.get(email=data["email"])
            otp_entry = PasswordResetOTP.objects.get(user=user, otp=data["otp"])
            if not otp_entry.is_valid():
                raise serializers.ValidationError({"otp": "The OTP has expired."})
        except (CustomUser.DoesNotExist, PasswordResetOTP.DoesNotExist):
            raise serializers.ValidationError({"otp": "Invalid OTP or email."})
        return data

    def save(self, **kwargs):
        user = CustomUser.objects.get(email=self.validated_data["email"])
        user.set_password(self.validated_data["new_password"])  # Hash the password
        user.save()
        PasswordResetOTP.objects.filter(
            user=user
        ).delete()  # Delete OTP after successful reset
        return user
