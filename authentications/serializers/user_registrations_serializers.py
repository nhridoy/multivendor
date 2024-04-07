import random

from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, validators

from authentications.models import User, UserInformation


class NewUserSerializer(serializers.ModelSerializer):
    """
    New User Registration Serializer
    """

    email = serializers.EmailField(
        required=True,
        validators=[
            validators.UniqueValidator(
                queryset=User.objects.all(),
                message="This email is already in use. Please use a different email.",
            )
        ],
    )

    password1 = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    password2 = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
        required=True,
        label="Retype Password",
    )

    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
        ]

    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise validators.ValidationError(
                {
                    "password1": "Password Doesn't Match",
                }
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=self.__create_username(validated_data["email"]),
            email=validated_data["email"],
        )
        user.set_password(validated_data["password1"])
        if not settings.OTP_ENABLED:
            user.is_verified = True
        user.save()

        user_info = UserInformation.objects.get(user=user)
        user_info.first_name = validated_data["first_name"]
        user_info.last_name = validated_data["last_name"]
        user_info.phone = validated_data["last_name"]

        user_info.save()
        return user

    def __create_username(self, email):
        """
        Create a unique username for the user.
        """
        username = email
        if username is None:
            return None
        username = username.split("@")[0]
        username = username.replace(".", "")
        username = username.replace("_", "")
        username = username.replace("-", "")
        username = username.lower()
        if username == "":
            return None
        if User.objects.filter(username=username).exists():
            username = username + str(random.randint(1, 1000))
        return username
