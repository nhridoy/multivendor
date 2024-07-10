import datetime
import random
from typing import Literal

from dj_rest_auth.jwt_auth import set_jwt_cookies
from django.conf import settings
from django.contrib.auth import login
from django.utils.translation import gettext as _
from pyotp import TOTP
from rest_framework import exceptions, response, status
from rest_framework_simplejwt.tokens import RefreshToken

from authentications.models import User
from utils.helper import encode_token, encrypt
from utils.modules import EmailSender
from utils.modules.solapi_sms import SolApiClient


def get_origin(self):
    try:
        return self.request.headers["origin"]
    except Exception as e:
        raise exceptions.PermissionDenied(
            detail=_("Origin not found on request header")
        ) from e


def direct_login(request, user: User, token_data):
    if settings.REST_AUTH.get("SESSION_LOGIN", False):
        login(request, user)

    resp = response.Response()

    set_jwt_cookies(
        response=resp,
        access_token=token_data.get(
            settings.REST_AUTH.get("JWT_AUTH_COOKIE", "access"),
        ),
        refresh_token=token_data.get(
            settings.REST_AUTH.get("JWT_AUTH_REFRESH_COOKIE", "refresh"),
        ),
    )
    resp.data = {"data": token_data, "detail": _("Logged in successfully")}
    resp.status_code = status.HTTP_200_OK
    return resp


def generate_and_send_otp(
    user: User, otp_method: Literal["sms", "email"], generate_secret: bool = False
):
    otp = TOTP(user.user_two_step_verification.secret_key, interval=300)

    otp_code = otp.now()
    if otp_method == "sms":
        # sms send for otp code
        send_verification_sms(user.user_information.phone_number, otp_code)
    elif otp_method == "email":
        # email send for otp code
        send_otp_email(user, otp_code)

    return response.Response(
        {
            "data": {
                "secret": generate_token(user) if generate_secret else None,
                "otp_method": otp_method,
                "detail": _("OTP is active for 300 seconds"),
            },
            "message": _("OTP is Sent"),
        },
        status=status.HTTP_200_OK,
    )


def generate_link(user: User, origin: str, route: str) -> str:
    return f"{origin}/auth/{route}/{generate_token(user)}/"


def generate_token(user: User):
    payload = {
        "user": str(user.id),
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(seconds=settings.TOKEN_TIMEOUT_SECONDS),
    }
    token = encrypt(encode_token(payload=payload)).decode()
    return token


def generate_otp(user: User):
    otp = f"{user.id}{random.randint(10000, 99999)}"
    return otp


def send_otp_email(user, otp):
    body = f"One time verification code is {otp}"
    email = EmailSender(send_to=[user.email], subject="OTP Verification", body=body)
    email.send_email()


def send_verification_email(user, link):
    body = f"Your Verification is {link}"
    email = EmailSender(send_to=[user.email], subject="OTP Verification", body=body)
    email.send_email()


def send_verification_sms(phone_number, code):
    body = f"One time verification code is {code}"
    solapi = SolApiClient()
    solapi.send_one(phone_number, body)
    # solapi.get_balance()
    print(body)


def get_token(user):
    token = RefreshToken.for_user(user)
    token["email"] = user.email
    token["is_staff"] = user.is_staff
    token["is_active"] = user.is_active
    token["is_superuser"] = user.is_superuser
    return token
