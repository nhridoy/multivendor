import os
import random
from uuid import uuid4

import requests
from django.contrib.auth import authenticate
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db.models import Q
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from authentications.models import User


def save_image_from_url(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(response.content)
        img_temp.flush()
        return img_temp


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def generate_username(name):
    username = "".join(name.split(" ")).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_social_user(profile_image_url, provider, email, name):
    filtered_user = User.objects.filter(email=email)

    if len(filtered_user):

        if provider == filtered_user[0].oauth_provider:

            tokens = get_tokens_for_user(user=filtered_user[0])

            return tokens

        else:
            raise AuthenticationFailed(
                detail="Please continue your login using "
                + filtered_user[0].oauth_provider
            )

    else:
        user = {
            "username": generate_username(name),
            "email": email,
            "oauth_provider": provider,
        }
        user = User.objects.create_user(**user)
        user.user_information.full_name = name
        # Save profile picture from URL
        if profile_image_url:
            image_temp = save_image_from_url(profile_image_url)
            user.user_information.profile_picture.save(str(uuid4()), File(image_temp))
        user.user_information.save(update_fields=["full_name", "profile_picture"])

        tokens = get_tokens_for_user(user=user)
        return tokens
