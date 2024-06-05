from rest_framework import serializers


class PushNotificationSerializer(serializers.Serializer):
    title = serializers.CharField()
    body = serializers.CharField()
    image = serializers.URLField(required=False)
