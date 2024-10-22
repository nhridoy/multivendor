import contextlib

from rest_framework import serializers

from authentications.serializers import UserSerializer
from support.models import Inquiry, InquiryAnswer


class InquirySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Inquiry
        fields = ("id", "user", "title", "body", "created_at", "is_answered")
        read_only_fields = ("is_answered",)


class InquiryAnswerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = InquiryAnswer
        fields = ("id", "user", "inquiry", "answer", "created_at")
        read_only_fields = ("inquiry",)
