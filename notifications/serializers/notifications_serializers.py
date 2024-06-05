from rest_framework.serializers import ModelSerializer

from notifications.models import Notifications, Groups, NotificationsGroup


class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notifications
        fields = "__all__"


class GroupsSerializer(ModelSerializer):
    class Meta:
        model = Groups
        fields = "__all__"


class NotificationsGroupSerializer(ModelSerializer):
    class Meta:
        model = NotificationsGroup
        fields = "__all__"
