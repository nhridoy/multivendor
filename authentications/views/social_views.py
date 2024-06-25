import json
import time
from datetime import timedelta

import jwt
import requests
import requests.exceptions
from django.conf import settings
from django.utils import timezone
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from jwt.algorithms import RSAAlgorithm
from rest_framework import exceptions, response, views
from social_core.backends.apple import AppleIdAuth
from social_core.backends.google import GoogleOAuth2
from social_core.backends.kakao import KakaoOAuth2

from authentications.register import register_social_user, save_image_from_url
from authentications.serializers import SocialLoginSerializer


class GoogleLoginView(views.APIView):
    permission_classes = ()
    authentication_classes = ()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "code",
                type={"type": "string"},
                style="form",
                explode=False,
                required=True,
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        serializer = SocialLoginSerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        google_backend = GoogleOAuth2()
        try:
            data = {
                "code": serializer.validated_data.get("code"),
                "client_id": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
                "client_secret": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URL,
                "grant_type": "authorization_code",
            }
            resp = requests.post(settings.GOOGLE_TOKEN_URL, data=data)

            print(resp.json())

            user_data = google_backend.user_data(resp.json().get("access_token"))
            print(user_data)

        except requests.exceptions.HTTPError as e:
            raise exceptions.AuthenticationFailed(detail=e) from e

        tokens = register_social_user(
            profile_image_url=user_data.get("picture"),
            email=user_data.get("email"),
            name=user_data.get("name"),
            provider="google",
        )

        return response.Response(tokens)


class KakaoLoginView(views.APIView):
    permission_classes = ()
    authentication_classes = ()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "code",
                type={"type": "string"},
                style="form",
                explode=False,
                required=True,
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        serializer = SocialLoginSerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        kakao_backend = KakaoOAuth2()
        try:
            data = {
                "code": serializer.validated_data.get("code"),
                "client_id": settings.SOCIAL_AUTH_KAKAO_APP_KEY,
                "redirect_uri": settings.KAKAO_REDIRECT_URL,
                "grant_type": "authorization_code",
            }
            resp = requests.post(settings.KAKAO_TOKEN_URL, data=data)

            user_data = kakao_backend.user_data(resp.json().get("access_token"))

        except requests.exceptions.HTTPError as e:
            raise exceptions.AuthenticationFailed(detail=e) from e

        tokens = register_social_user(
            profile_image_url=user_data.get("kakao_account")
            .get("profile")
            .get("profile_image_url"),
            email=user_data.get("kakao_account").get("email"),
            name=user_data.get("kakao_account").get("profile").get("nickname"),
            provider="kakao",
        )

        return response.Response(tokens)


class AppleLoginView(views.APIView):
    permission_classes = ()
    authentication_classes = ()

    def get_key_and_secret(self):
        headers = {"kid": settings.SOCIAL_AUTH_APPLE_ID_KEY}
        payload = {
            "iss": settings.SOCIAL_AUTH_APPLE_ID_TEAM,
            "iat": timezone.now(),
            "exp": timezone.now() + timedelta(days=180),
            "aud": "https://appleid.apple.com",
            "sub": settings.SOCIAL_AUTH_APPLE_ID_CLIENT,
        }

        client_secret = jwt.encode(
            payload,
            key=settings.SOCIAL_AUTH_APPLE_ID_SECRET,
            algorithm="ES256",
            headers=headers,
        )

        return client_secret

    def post(self, request, *args, **kwargs):
        request_data = self.request.data
        serializer = SocialLoginSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        try:
            data = {
                "code": serializer.validated_data.get("code"),
                "client_id": settings.SOCIAL_AUTH_APPLE_ID_CLIENT,
                "client_secret": self.get_key_and_secret(),
                "redirect_uri": settings.APPLE_REDIRECT_URL,
                "grant_type": "authorization_code",
            }
            resp = requests.post(
                settings.APPLE_TOKEN_URL,
                data=data,
                headers={"content-type": "application/x-www-form-urlencoded"},
            )

            if resp.status_code == 200:
                decoded = jwt.decode(
                    resp.json().get("id_token"),
                    audience=settings.SOCIAL_AUTH_APPLE_ID_CLIENT,
                    options={"verify_signature": False},
                )

                user = json.loads(request_data.get("user", "{}"))

                full_name = (
                    (
                        f"{user.get('name').get('firstName')} {user.get('name').get('lastName')}"
                    )
                    if len(user)
                    else ""
                )
                email = user.get("email") or decoded.get("email")

                tokens = register_social_user(
                    profile_image_url=None,
                    email=email,
                    name=full_name,
                    provider="apple",
                )
                return response.Response(tokens)

            else:
                raise exceptions.AuthenticationFailed(detail=resp.json())

        except requests.exceptions.HTTPError as e:
            raise exceptions.AuthenticationFailed(detail=e) from e
