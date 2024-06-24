from django.conf import settings
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from authentications.models import UserTwoStepVerification


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


class OTPCheckSerializer(serializers.ModelSerializer):
    """
    Serializer for checking if OTP is active or not
    """

    # detail = serializers.BooleanField(read_only=True)

    class Meta:
        model = UserTwoStepVerification
        fields = ["is_active"]
