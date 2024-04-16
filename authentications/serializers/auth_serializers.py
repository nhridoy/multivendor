from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import contextlib

from django.conf import settings
from django.contrib.auth import authenticate
from django.urls import exceptions as url_exceptions
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework_simplejwt import settings as jwt_settings, tokens
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from authentications.models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        return data

    def get_token(self, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        token['is_active'] = user.is_active
        token['is_superuser'] = user.is_superuser
        return token
