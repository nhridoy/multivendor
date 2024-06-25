from cryptography.fernet import InvalidToken as FernetInvalidToken
from django.conf import settings
from django.contrib.auth.models import update_last_login
from jwt import ExpiredSignatureError
from pyotp import HOTP
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
    secret = serializers.CharField(write_only=True)
    otp = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.payload = None

    def validate_secret(self, value):
        try:
            self.payload = decode_token(decrypt(value))
        except FernetInvalidToken as e:
            raise serializers.ValidationError("Invalid OTP Secret") from e
        except ExpiredSignatureError as e:
            raise serializers.ValidationError("OTP Secret Expired") from e
        return value

    def validate_otp(self, value):
        if not bool(self.payload):
            raise serializers.ValidationError("OTP Secret must be validated first")

        request = self.context.get("request")
        otp = HOTP(request.user.user_two_step_verification.secret_key)
        if not otp.verify(value, self.payload.get("rand")):
            raise serializers.ValidationError("Invalid OTP")
        return value


class LogoutSerializer(serializers.Serializer):
    device_id = serializers.CharField(write_only=True)
