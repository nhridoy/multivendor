import random

from django.conf import settings
from django.contrib.auth.password_validation import (
    validate_password as validate_input_password,
)
from rest_framework import serializers, validators

from authentications.models import ROLE, User, UserInformation


class RegistrationSerializer(serializers.ModelSerializer):
    """
    New User Registration Serializer
    """

    retype_password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
        required=True,
        label="Retype Password",
    )

    full_name = serializers.CharField(
        required=True, write_only=True, source="user_information.full_name"
    )
    role = serializers.ChoiceField(
        choices=ROLE,
        required=True,
        write_only=True,
    )

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "retype_password",
            "full_name",
            "role",
        ]

    def validate_password(self, value):
        attrs = self.get_initial()

        if attrs.get("password") != attrs.get("retype_password"):
            raise serializers.ValidationError("Password fields didn't match.")

        # You can add additional password validation here
        validate_input_password(
            password=attrs.get("password"),
            user=User(email=attrs.get("email")),
        )

        return value

    def create(self, validated_data):
        information_user = validated_data.pop("user_information")
        validated_data.pop("retype_password")
        user = User.objects.create_user(**validated_data, oauth_provider="email")
        user_info = user.user_information
        user_info.full_name = information_user["full_name"]

        user_info.save(update_fields=["full_name"])

        return user
