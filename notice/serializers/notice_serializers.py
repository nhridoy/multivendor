from rest_framework.serializers import ModelSerializer

from notice.models import Notice, NoticeType, NoticeRecipient


class NoticeTypeSerializer(ModelSerializer):
    class Meta:
        model = NoticeType
        fields = "__all__"


class NoticeSerializer(ModelSerializer):
    class Meta:
        model = Notice
        fields = "__all__"


class NoticeRecipientSerializer(ModelSerializer):
    class Meta:
        model = NoticeRecipient
        fields = "__all__"
