import datetime
import random

from dj_rest_auth.jwt_auth import set_jwt_cookies
from django.conf import settings
from django.contrib.auth import login
from pyotp import TOTP
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from authentications.models import User
from utils.helper import decode_token, decrypt, encode_token, encrypt
from utils.modules import EmailSender
from utils.modules.solapi_sms import SolApiClient


def direct_login(request, user: User, token_data):
    if settings.REST_AUTH.get("SESSION_LOGIN", False):
        login(request, user)

    resp = Response()

    set_jwt_cookies(
        response=resp,
        access_token=token_data.get(
            settings.REST_AUTH.get("JWT_AUTH_COOKIE", "access"),
        ),
        refresh_token=token_data.get(
            settings.REST_AUTH.get("JWT_AUTH_REFRESH_COOKIE", "refresh"),
        ),
    )
    resp.data = {"data": token_data, "detail": "Logged in successfully"}
    resp.status_code = status.HTTP_200_OK
    return resp


def otp_login(user: User):
    otp = TOTP(user.user_two_step_verification.secret_key, interval=300)

    payload = {
        "type": "otp",
        "user": str(user.id),
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(minutes=5),
    }

    token = encrypt(encode_token(payload))
    otp_code = otp.now()
    # email send for otp code
    send_otp_email(user, otp_code)

    return Response(
        {"secret": token.decode(), "detail": "OTP is Sent"}, status=status.HTTP_200_OK
    )


def generate_link(user: User, origin: str, route: str) -> str:
    payload = {
        "user": str(user.id),
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(minutes=30),
    }

    return f"{origin}/auth/{route}/{encrypt(encode_token(payload=payload)).decode()}/"


def generate_token(user: User):
    payload = {
        "user": str(user.id),
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(minutes=30),
    }
    token = encrypt(encode_token(payload=payload)).decode()
    return token


def generate_otp(user: User):
    otp = f"{user.id}{random.randint(10000, 99999)}"
    return otp


def send_otp_email(user, otp):
    body = f"Your OTP code is {otp}"
    email = EmailSender(send_to=[user.email], subject="OTP Verification", body=body)
    email.send_email()


def send_verification_email(user, link):
    body = f"Your Verification is {link}"
    email = EmailSender(send_to=[user.email], subject="OTP Verification", body=body)
    email.send_email()


def send_verification_sms(phone_number, code):
    body = f"Your Verification code is {code}"
    solapi = SolApiClient()
    solapi.send_one(phone_number, body)
    # solapi.get_balance()
    print(body)


def get_token(user):
    token = RefreshToken.for_user(user)
    token["username"] = user.username
    token["email"] = user.email
    token["is_staff"] = user.is_staff
    token["is_active"] = user.is_active
    token["is_superuser"] = user.is_superuser
    return token
