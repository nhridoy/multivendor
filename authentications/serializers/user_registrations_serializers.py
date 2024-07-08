import random

from django.conf import settings
from django.contrib.auth.password_validation import (
    validate_password as validate_input_password,
)
from rest_framework import serializers, validators

from authentications.models import ROLE, User, UserInformation


class NewUserSerializer(serializers.ModelSerializer):
    """
    New User Registration Serializer
    """

    first_name = serializers.CharField(
        required=True, write_only=True, source="user_information.first_name"
    )
    last_name = serializers.CharField(
        required=True, write_only=True, source="user_information.last_name"
    )
    retype_password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
        required=True,
        label="Retype Password",
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
            "first_name",
            "last_name",
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

        user_info.first_name = information_user["first_name"]
        user_info.last_name = information_user["last_name"]

        user_info.save(update_fields=["first_name", "last_name"])

        return user
