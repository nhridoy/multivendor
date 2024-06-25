from cryptography.fernet import InvalidToken as FernetInvalidToken
from django.conf import settings
from django.contrib.auth.models import update_last_login
from jwt import ExpiredSignatureError
from pyotp import HOTP, TOTP
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from utils.helper import decode_token, decrypt


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        if settings.SIMPLE_JWT.get("UPDATE_LAST_LOGIN"):
            update_last_login(None, self.user)

        return data, self.user

    def get_token(self, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["email"] = user.email
        token["is_staff"] = user.is_staff
        token["is_active"] = user.is_active
        token["is_superuser"] = user.is_superuser
        return token


class OTPSerializer(serializers.Serializer):
    otp = serializers.CharField(write_only=True)
    otp_method = serializers.ChoiceField(
        choices=["authenticator_app", "email", "sms"],
        write_only=True,
        default="authenticator_app",
    )

    def validate_otp(self, value):
        request = self.context.get("request")
        if (
            self.initial_data.get("otp_method", "authenticator_app")
            == "authenticator_app"
        ):
            otp = TOTP(request.user.user_two_step_verification.secret_key)
            if not otp.verify(value):
                raise serializers.ValidationError("Invalid OTP")
        else:
            otp = TOTP(request.user.user_two_step_verification.secret_key, interval=300)
            if not otp.verify(value):
                raise serializers.ValidationError("Invalid OTP")
        return value


class LogoutSerializer(serializers.Serializer):
    device_id = serializers.CharField(write_only=True)
