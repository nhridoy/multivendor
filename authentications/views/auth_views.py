import contextlib

import fernet
from dj_rest_auth.jwt_auth import (
    set_jwt_access_cookie,
    set_jwt_refresh_cookie,
    unset_jwt_cookies,
)
from django.conf import settings
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from jwt.exceptions import DecodeError, ExpiredSignatureError, InvalidTokenError
from pyotp import HOTP
from rest_framework import exceptions, generics, permissions, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from authentications.models import User, UserTwoStepVerification
from authentications.permissions import IsAuthenticatedAndEmailVerified
from authentications.serializers import (  # TokenRefreshSerializer
    CustomTokenObtainPairSerializer,
    OTPCheckSerializer,
    OTPSerializer,
)
from utils.helper import decode_token, decrypt

from .helper import direct_login, get_token, otp_login


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user: User = serializer.validated_data[1]
            if user.user_two_step_verification.is_active:
                return otp_login(user)
            else:
                return direct_login(request, user, serializer.validated_data[0])

        except exceptions.AuthenticationFailed as e:
            raise exceptions.AuthenticationFailed(
                detail="Invalid username or password"
            ) from e

        except AssertionError as e:
            raise exceptions.APIException(detail=str(e))


class MyTokenRefreshView(generics.GenericAPIView):
    """
    View for get new access token for a valid refresh token
    """

    serializer_class = TokenRefreshSerializer
    permission_classes = ()
    authentication_classes = ()

    @staticmethod
    def _set_cookie(resp, serializer):
        if refresh := serializer.validated_data.get(
            settings.REST_AUTH.get("JWT_AUTH_REFRESH_COOKIE")
        ):  # noqa
            set_jwt_refresh_cookie(
                response=resp,
                refresh_token=refresh,
            )
        set_jwt_access_cookie(
            response=resp,
            access_token=serializer.validated_data.get(
                settings.REST_AUTH.get("JWT_AUTH_COOKIE")
            ),  # noqa
        )

    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get(
            settings.REST_AUTH.get("JWT_AUTH_REFRESH_COOKIE")
        ) or request.data.get(settings.REST_AUTH.get("JWT_AUTH_REFRESH_COOKIE"))

        serializer = self.serializer_class(
            data={settings.REST_AUTH.get("JWT_AUTH_REFRESH_COOKIE"): refresh}
        )
        serializer.is_valid(raise_exception=True)
        resp = Response()
        self._set_cookie(resp=resp, serializer=serializer)
        resp.data = serializer.validated_data
        resp.status_code = status.HTTP_200_OK
        return resp


class LogoutView(views.APIView):
    """
    Calls Django logout method and delete the Token object
    assigned to the current User object.

    Accepts/Returns nothing.
    """

    permission_classes = (permissions.IsAuthenticated,)
    throttle_scope = "dj_rest_auth"

    def get(self, request, *args, **kwargs):
        if getattr(settings, "ACCOUNT_LOGOUT_ON_GET", False):
            resp = self._logout(request)
        else:
            resp = self.http_method_not_allowed(request, *args, **kwargs)

        return self.finalize_response(request, resp, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self._logout(request)

    @staticmethod
    def _logout(request):
        with contextlib.suppress(AttributeError, ObjectDoesNotExist):
            request.user.auth_token.delete()

        if settings.REST_AUTH.get("SESSION_LOGIN", False):
            logout(request)

        resp = Response(
            {"detail": "Successfully logged out."},
            status=status.HTTP_200_OK,
        )

        if settings.REST_AUTH.get("USE_JWT", True):
            cookie_name = settings.REST_AUTH.get("JWT_AUTH_COOKIE", "access")

            unset_jwt_cookies(resp)

            if "rest_framework_simplejwt.token_blacklist" in settings.INSTALLED_APPS:
                # add refresh token to blacklist
                try:
                    token = RefreshToken(
                        request.COOKIES.get(
                            settings.REST_AUTH.get("JWT_AUTH_REFRESH_COOKIE")
                        )
                        or request.data.get(
                            settings.REST_AUTH.get("JWT_AUTH_REFRESH_COOKIE")
                        )
                    )
                    token.blacklist()
                except KeyError:
                    resp.data = {
                        "detail": "Refresh token was not included in request data."
                    }
                    resp.status_code = status.HTTP_401_UNAUTHORIZED
                except (TokenError, AttributeError, TypeError) as error:
                    if hasattr(error, "args"):
                        if (
                            "Token is blacklisted" in error.args
                            or "Token is invalid or expired" in error.args
                        ):
                            resp.data = {"detail": error.args[0]}
                            resp.status_code = status.HTTP_401_UNAUTHORIZED
                        else:
                            resp.data = {"detail": "An error has occurred."}
                            resp.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

                    else:
                        resp.data = {"detail": "An error has occurred."}
                        resp.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            elif not cookie_name:
                message = (
                    "Neither cookies or blacklist are enabled, so the token "
                    "has not been deleted server side. "
                    "Please make sure the token is deleted client side.",
                )
                resp.data = {"detail": message}
                resp.status_code = status.HTTP_200_OK
        return resp


class OTPLoginView(views.APIView):
    serializer_class = OTPSerializer
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            secret = decode_token(decrypt(serializer.validated_data.get("secret")))
            otp = serializer.validated_data.get("otp")
            rand = int(secret.get("rand"))

            user: User = generics.get_object_or_404(User, id=secret.get("user"))
            hotp = HOTP(user.user_two_step_verification.secret_key)

            if hotp.verify(otp, rand):
                token = get_token(user)
                return direct_login(
                    request,
                    user,
                    {
                        settings.REST_AUTH.get(
                            "JWT_AUTH_REFRESH_COOKIE", "refresh"
                        ): str(token),
                        settings.REST_AUTH.get("JWT_AUTH_COOKIE", "access"): str(
                            token.access_token
                        ),
                    },
                )
            else:
                raise ExpiredSignatureError("Wrong OTP")
        except ExpiredSignatureError as e:
            raise exceptions.AuthenticationFailed(detail=str(e)) from e
        except fernet.InvalidToken as e:
            raise InvalidToken(detail=str(e)) from e
        except DecodeError as e:
            raise InvalidToken(detail="Wrong Secret") from e
        except InvalidTokenError as e:
            raise exceptions.AuthenticationFailed(detail=str(e)) from e
        except TokenError as e:
            raise exceptions.AuthenticationFailed(detail=str(e)) from e
        except ValidationError as e:
            raise exceptions.APIException(detail="Validation error") from e


class OTPCheckView(views.APIView):
    """
    Check if OTP is active for user or not
    """

    permission_classes = (IsAuthenticatedAndEmailVerified,)
    serializer_class = OTPCheckSerializer

    def get(self, request, *args, **kwargs):
        try:
            user_otp = generics.get_object_or_404(
                UserTwoStepVerification, user=self.request.user
            )
            serializer = self.serializer_class(user_otp)
            return Response(
                {
                    "data": [serializer.data.get("is_active")],
                    "detail": serializer.data.get("is_active"),
                }
            )
        except Exception as e:
            raise exceptions.APIException from e


class OTPView(views.APIView):
    """
    Get method for OTP Create
    Post method for OTP verify
    Delete method for Disabling OTP
    """

    permission_classes = (IsAuthenticatedAndEmailVerified,)

    # serializer_class = serializers.OTPCreateSerializer
    def get_serializer_class(self):
        if self.request.method == "POST":
            return OTPSerializer

    @staticmethod
    def _clear_user_otp(user_otp):
        user_otp.is_active = False
        user_otp.save()

    def get(self, request, *args, **kwargs):
        return otp_login(self.request.user)

    def post(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            secret = decode_token(decrypt(serializer.validated_data.get("secret")))
            user_otp = self.request.user.user_two_step_verification
            hotp = HOTP(user_otp.secret_key)
            if hotp.verify(
                serializer.validated_data.get("otp"), int(secret.get("rand"))
            ):
                user_otp.is_active = True
                user_otp.save()
                return Response(
                    {
                        "data": {"detail": "OTP is activated"},
                        "message": "OTP is activated",
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                self._clear_user_otp(user_otp)
                raise exceptions.NotAcceptable(detail="OTP is Wrong or Expired!!!")
        except fernet.InvalidToken as e:
            raise InvalidToken(detail=str(e)) from e
        except ExpiredSignatureError as e:
            raise exceptions.AuthenticationFailed(detail=str(e)) from e

    def delete(self, request, *args, **kwargs):
        current_user = self.request.user
        user_otp = UserTwoStepVerification.objects.get(user=current_user)
        self._clear_user_otp(user_otp)
        return Response({"data": {"detail": "OTP Removed"}, "message": "OTP Removed"})
