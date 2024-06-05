import json

import pyotp
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from authentications.models import User
from utils import helper


class PasswordValidateSerializer(serializers.Serializer):
    """
    Serializer for validating password
    """

    password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
        required=True,
    )


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """

    old_password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
        required=True,
    )
    password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
        required=True,
    )
    retype_password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
        required=True,
    )


# ============***********============
# Password reset serializer
# ============***********============
class EmailSerializer(serializers.Serializer):
    """
    Reset Password Email Request Serializer.
    """

    email = serializers.EmailField(required=True)

    class Meta:
        fields = ("email",)


# ============***********============
# OTP BASED SERIALIZER PASSWORD RESET
# ============***********============
class PasswordResetVerifySerializer(serializers.Serializer):
    one_time_password = serializers.CharField()

    def validate_one_time_password(self, value):
        token = self.context.get("token")
        user, otp, _decrypted_data = self._validate_user(token)
        print()
        if otp != value:
            raise serializers.ValidationError("OTP Invalid")
        hotp = pyotp.HOTP(user.user_two_step_verification.secret_key)
        if not hotp.verify(value, 1):
            raise serializers.ValidationError("Invalid one-time password")
        return self._verify_otp(_decrypted_data)

    def _validate_user(self, token):
        """
        Verify token and encoded_pk and then set new password.
        """

        _decrypted_data = helper.decode(token)
        _decrypted_data_dict = json.loads(_decrypted_data.replace("'", '"'))

        token = _decrypted_data_dict["token"]
        encoded_pk = _decrypted_data_dict["enc_pk"]
        otp = _decrypted_data_dict["otp"]

        if token is None or encoded_pk is None:
            raise serializers.ValidationError("Missing data.")

        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = User.objects.get(pk=pk)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("The reset token is invalid")
        return user, otp, _decrypted_data_dict

    def _verify_otp(self, _decrypted_data):
        _decrypted_data["verified"] = "True"
        _decrypted_data["verify_secret"] = settings.OTP_VERIFY_SECRET
        return helper.encode(str(_decrypted_data))

    def to_representation(self, instance):
        response = super(PasswordResetVerifySerializer, self).to_representation(
            instance
        )
        token = response.pop("one_time_password").split("'")[1]
        response["token"] = token
        return response


class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    new_password_confirm = serializers.CharField()

    def validate(self, data):
        try:
            token = self.context.get("token")
            user = self.__validate_user_token(token)
            if data["new_password"] != data["new_password_confirm"]:
                raise serializers.ValidationError("Passwords do not match.")
            user.set_password(data["new_password"])
            user.save()
            return data
        except:
            raise serializers.ValidationError("Invalid token or something went wrong.")

    def __validate_user_token(self, token):
        _decrypted_data = helper.decode(token)

        _decrypted_data_dict = json.loads(_decrypted_data.replace("'", '"'))

        token = _decrypted_data_dict["token"]

        encoded_pk = _decrypted_data_dict["enc_pk"]

        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = User.objects.get(pk=pk)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("The reset token is invalid")
        return user

    def _validate_user(self, token):  # for otp verification
        """
        Verify token and encoded_pk and then set new password.
        """

        _decrypted_data = helper.decode(token)
        _decrypted_data_dict = json.loads(_decrypted_data.replace("'", '"'))
        token = _decrypted_data_dict["token"]
        encoded_pk = _decrypted_data_dict["enc_pk"]
        verified = _decrypted_data_dict["verified"]
        verify_secret = _decrypted_data_dict["verify_secret"]
        if self._validate_otp_verified(verified, verify_secret):
            if token is None or encoded_pk is None:
                raise serializers.ValidationError("Missing data.")

            pk = urlsafe_base64_decode(encoded_pk).decode()
            user = User.objects.get(pk=pk)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("The reset token is invalid")
            return user
        raise serializers.ValidationError("OTP not verified")

    def _validate_otp_verified(self, verified, verify_secret):
        return bool(verified and verify_secret == settings.OTP_VERIFY_SECRET)
