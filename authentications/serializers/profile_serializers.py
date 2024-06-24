from django.db import transaction
from django.db.models import Avg
from rest_framework import serializers
from options.serializers import (
    CitySerializer,
    CountrySerializer,
    LanguageSerializer,
    ProvinceSerializer,
)
from authentications.models import (
    User,
    UserInformation,
    UserTwoStepVerification,
)


class UserInformationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = UserInformation
        fields = (
            "username",
            "email",
            "full_name",
            "nationality",
            "interests",
            "province",
            "city",
            "visa_type",
            "language",
            "profile_picture",
            "date_of_birth",
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        # remove city information from the province if province is not null
        if instance.province:
            ret["province"] = ProvinceSerializer(instance.province).data
            ret["province"].pop("cities")
        if instance.city:
            ret["city"] = CitySerializer(instance.city).data
        if instance.nationality:
            ret["nationality"] = CountrySerializer(instance.nationality).data
        if instance.language:
            ret["language"] = LanguageSerializer(instance.language).data
        return ret


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user_information.name")
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
            "username",
            "email",
            "phone_number",
            "name",
            "profile_picture",
            "date_of_birth",
            "gender",
            "address",
            "oauth_provider",
            "date_joined",
            "is_active",
            "is_staff",
            # "user_information"
        )
        read_only_fields = (
            "date_joined",
            "is_active",
            "id",
            "username",
            "email",
            "oauth_provider",
            "is_staff",
        )

    @transaction.atomic
    def update(self, instance, validated_data):
        if information_user := validated_data.pop("user_information", None):
            # Update the UserInformation fields or related object
            user_information = instance.user_information
            for key, value in information_user.items():
                setattr(user_information, key, value)
            user_information.save()

        return instance


class SendInvitationSerializer(serializers.Serializer):
    email = serializers.ListField(child=serializers.EmailField())
