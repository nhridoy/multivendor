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
from social_core.backends.github import GithubOAuth2
from social_core.backends.google import GoogleOAuth2
from social_core.backends.kakao import KakaoOAuth2
from social_core.backends.naver import NaverOAuth2
from social_django.utils import load_strategy

from authentications.register import register_social_user, save_image_from_url
from authentications.serializers import SocialLoginSerializer

from .common_functions import extract_token, get_token


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
        strategy = load_strategy(request)
        google_backend = GoogleOAuth2(strategy=strategy)
        try:
            data = {
                "code": serializer.validated_data.get("code"),
                "client_id": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
                "client_secret": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
                "redirect_uri": request.build_absolute_uri("/api/auth/google/"),
                "grant_type": "authorization_code",
            }
            resp = requests.post(settings.GOOGLE_TOKEN_URL, data=data)

            print(resp.json())

            user_data = google_backend.user_data(resp.json().get("access_token"))
            print(user_data)

        except requests.exceptions.HTTPError as e:
            raise exceptions.AuthenticationFailed(detail=e) from e

        user = register_social_user(
            profile_image_url=user_data.get("picture"),
            email=user_data.get("email"),
            name=user_data.get("name"),
            provider="google",
            role="user",
        )

        return response.Response(extract_token(get_token(user)))


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
            ),
            OpenApiParameter(
                "type",
                enum=["web", "ios", "android"],
                type={"type": "string"},
                style="form",
                explode=False,
                required=True,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        request_data = self.request.query_params
        serializer = SocialLoginSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        strategy = load_strategy(request)
        kakao_backend = KakaoOAuth2(strategy=strategy)
        try:
            if request_data.get("type", "web") == "web":
                data = {
                    "code": serializer.validated_data.get("code"),
                    "client_id": settings.SOCIAL_AUTH_KAKAO_APP_KEY,
                    "redirect_uri": request.build_absolute_uri("/api/auth/kakao/"),
                    "grant_type": "authorization_code",
                }
                resp = requests.post(settings.KAKAO_TOKEN_URL, data=data)

                user_data = kakao_backend.user_data(resp.json().get("access_token"))
            else:
                user_data = kakao_backend.user_data(
                    serializer.validated_data.get("code")
                )

        except requests.exceptions.HTTPError as e:
            raise exceptions.AuthenticationFailed(detail=e) from e

        user = register_social_user(
            profile_image_url=user_data.get("kakao_account")
            .get("profile")
            .get("profile_image_url"),
            email=user_data.get("kakao_account").get("email"),
            name=user_data.get("kakao_account").get("profile").get("nickname"),
            provider="kakao",
            role="user",
        )

        return response.Response(extract_token(get_token(user)))


"""
Not tested
"""


class NaverLoginView(views.APIView):
    permission_classes = ()
    authentication_classes = ()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "access_token",
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
        strategy = load_strategy(request)
        naver_backend = NaverOAuth2(strategy=strategy)
        access_token = serializer.validated_data.get("access_token")

        user_data = naver_backend.user_data(access_token)

        user = register_social_user(
            profile_image_url=user_data.get("profile_image"),
            email=user_data.get("email"),
            name=user_data.get("nickname"),
            provider="naver",
            role="student",
        )

        return response.Response(extract_token(get_token(user)))


"""
Not tested
"""


class GithubLoginView(views.APIView):
    permission_classes = ()
    authentication_classes = ()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "access_token",
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
        strategy = load_strategy(request)
        github_backend = GithubOAuth2(strategy=strategy)
        user_data = github_backend.user_data(
            serializer.validated_data.get("access_token")
        )
        user = register_social_user(
            profile_image_url=user_data.get("avatar_url"),
            email=user_data.get("email"),
            name=user_data.get("name")
            or user_data.get("login"),  # GitHub might not provide name
            provider="github",
            role="student",
        )

        return response.Response(extract_token(get_token(user)))


class AppleLoginView(views.APIView):
    permission_classes = ()
    authentication_classes = ()

    def get_key_and_secret(self, client_id):
        headers = {"kid": settings.SOCIAL_AUTH_APPLE_ID_KEY}
        payload = {
            "iss": settings.SOCIAL_AUTH_APPLE_ID_TEAM,
            "iat": timezone.now(),
            "exp": timezone.now() + timedelta(days=180),
            "aud": "https://appleid.apple.com",
            "sub": client_id,
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
        client_type = request_data.get("type", "web")
        client_id = (
            settings.SOCIAL_AUTH_APPLE_ID_SERVICE
            if client_type == "web"
            else settings.SOCIAL_AUTH_APPLE_ID_CLIENT
        )
        serializer = SocialLoginSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        try:
            data = {
                "code": serializer.validated_data.get("code"),
                "client_id": client_id,
                "client_secret": self.get_key_and_secret(client_id),
                "redirect_uri": request.build_absolute_uri("/api/auth/apple/"),
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
                    audience=client_id,
                    options={"verify_signature": False},
                )

                user = (
                    request_data.get("user", {})
                    if client_type == "web"
                    else json.loads(request_data.get("user", "{}"))
                )

                full_name = (
                    (
                        f"{user.get('name').get('firstName')} {user.get('name').get('lastName')}"
                    )
                    if len(user)
                    else ""
                )
                email = user.get("email") or decoded.get("email")

                user = register_social_user(
                    profile_image_url=None,
                    email=email,
                    name=full_name,
                    provider="apple",
                    role="user",
                )
                return response.Response(extract_token(get_token(user)))

            else:
                raise exceptions.AuthenticationFailed(detail=resp.json())

        except requests.exceptions.HTTPError as e:
            raise exceptions.AuthenticationFailed(detail=e) from e
