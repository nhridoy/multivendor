from rest_framework import serializers


class SocialLoginSerializer(serializers.Serializer):
    code = serializers.CharField()