from django.conf import settings
from fernet import Fernet


def encode(data: str):
    key = bytes(settings.ENC_SECRET_KEY, "utf-8")
    return Fernet(key).encrypt(bytes(data, "utf-8"))


def decode(token: str):
    key = bytes(settings.ENC_SECRET_KEY, "utf-8")
    return Fernet(key).decrypt(bytes(token, "utf-8")).decode("utf-8")
