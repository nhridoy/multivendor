import contextlib

from django.db import transaction
from django.db.models import Avg
from rest_framework import serializers

from authentications.models import User, UserInformation, UserTwoStepVerification
from options.models import City, Country, Language, Province
from options.serializers import (
    CitySerializer,
    CountrySerializer,
    LanguageSerializer,
    ProvinceSerializer,
)

from .helper_functions import update_related_instance


class UserInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInformation
        fields = (
            "full_name",
            "gender",
            "country",
            "province",
            "city",
            "language",
            "profile_picture",
            "date_of_birth",
        )


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="user_information.full_name")
    profile_picture = serializers.ImageField(source="user_information.profile_picture")
    date_of_birth = serializers.DateField(source="user_information.date_of_birth")
    gender = serializers.ChoiceField(
        source="user_information.gender", choices=UserInformation.GENDER
    )
    address = serializers.CharField(source="user_information.address")
    phone_number = serializers.CharField(
        source="user_information.phone_number", read_only=True
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "phone_number",
            "full_name",
            "profile_picture",
            "date_of_birth",
            "gender",
            "address",
            "oauth_provider",
            "date_joined",
            "is_active",
            "is_staff",
        )
        read_only_fields = (
            "date_joined",
            "is_active",
            "id",
            "email",
            "oauth_provider",
            "is_staff",
        )

    @transaction.atomic
    def update(self, instance, validated_data):
        if information_user := validated_data.pop("user_information", None):
            # Update the UserInformation fields or related object
            update_related_instance(instance, information_user, "user_information")

        return instance


class PersonalProfileSerializer(UserSerializer):
    country = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(),
        source="user_information.country",
        required=False,
    )
    province = serializers.PrimaryKeyRelatedField(
        queryset=Province.objects.all(),
        source="user_information.province",
        required=False,
    )
    city = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(),
        source="user_information.city",
        required=False,
    )
    language = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.all(),
        source="user_information.language",
        required=False,
    )
    phone_number = serializers.CharField(source="user_information.phone_number")

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + (
            "country",
            "province",
            "city",
            "language",
            "phone_number",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["country"] = CountrySerializer(instance.user_information.country).data
        data["province"] = ProvinceSerializer(instance.user_information.province).data
        with contextlib.suppress(AttributeError, KeyError):
            data["province"].pop("cities")
        data["city"] = CitySerializer(instance.user_information.city).data
        data["language"] = LanguageSerializer(instance.user_information.language).data
        return data


class SendInvitationSerializer(serializers.Serializer):
    email = serializers.ListField(child=serializers.EmailField())
