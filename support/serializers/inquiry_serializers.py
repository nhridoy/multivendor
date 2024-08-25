import contextlib

from rest_framework import serializers

from support.models import Inquiry, InquiryAnswer


class InquirySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Inquiry
        fields = ("id", "user", "title", "body", "created_at", "is_answered")
        read_only_fields = ("is_answered",)

    def get_user(self, obj):
        print(obj)
        request = self.context.get("request")
        return {
            "id": obj.user.id,
            "full_name": obj.user.user_information.full_name,
            "profile_picture": (
                request.build_absolute_uri(
                    obj.user.user_information.profile_picture.url
                )
                if obj.user.user_information.profile_picture
                else None
            ),
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if self.context.get("view").action == "retrieve":
            with contextlib.suppress(Inquiry.answer.RelatedObjectDoesNotExist):
                representation["answer"] = instance.answer.answer
                representation["answer_time"] = instance.answer.created_at
        return representation


class InquiryAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = InquiryAnswer
        fields = ("id", "inquiry", "answer")
        read_only_fields = ("inquiry",)
