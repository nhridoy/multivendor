import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Permission, PermissionsMixin
from django.contrib.contenttypes.models import ContentType

from authentications.user_manager import UserManager


# ========****************========
# Custom authentications user model
# ========****************========


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model Class
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        verbose_name="ID",
    )
    username = models.CharField(
        max_length=100,
        verbose_name="Username",
        unique=True,
    )
    email = models.EmailField(
        max_length=100,
        verbose_name="Email",
        unique=True,
        null=True,
        blank=True,
    )
    phone_number = models.CharField(
        max_length=50,
        verbose_name="Phone Number",
        blank=True,
        null=True,
    )

    date_joined = models.DateTimeField(
        verbose_name="Date Joined",
        auto_now_add=True,
    )
    last_login = models.DateTimeField(auto_now=True)

    # user role
    is_superuser = models.BooleanField(
        verbose_name="Superuser Status",
        default=False,
        help_text="Designate if the " "user has superuser " "status",
    )
    is_staff = models.BooleanField(
        verbose_name="Staff Status",
        default=False,
        help_text="Designate if the user has " "staff status",
    )
    is_active = models.BooleanField(
        verbose_name="Active Status",
        default=True,
        help_text="Designate if the user has " "active status",
    )
    is_verified = models.BooleanField(
        verbose_name="Email Verified",
        default=False,
        help_text="Email Verified",
    )
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "email",
    ]

    objects = UserManager()
