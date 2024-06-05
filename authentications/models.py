import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Permission, PermissionsMixin
from django.contrib.contenttypes.models import ContentType

from authentications.user_manager import UserManager

# ========****************========
# Custom authentications user model
# ========****************========
from core.models import BaseModel
from utils.helper import content_file_path


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model Class for Authentication
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


class UserInformation(BaseModel):
    """
    User Information Model
    to store user information like first name, last name, address, date of birth, phone number, etc.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_information")
    first_name = models.CharField(max_length=100, verbose_name="First Name", blank=True, null=True)
    last_name = models.CharField(max_length=100, verbose_name="Last Name", blank=True, null=True)
    profile_picture = models.ImageField(upload_to=content_file_path, blank=True, null=True)
    address = models.TextField(verbose_name="Address", blank=True, null=True)
    date_of_birth = models.DateField(verbose_name="Date of Birth", blank=True, null=True)
    phone_number = models.CharField(max_length=50, verbose_name="Phone Number", blank=True, null=True)


class UserTwoStepVerification(BaseModel):
    """
    User Two Step Verification Model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_two_step_verification")
    is_active = models.BooleanField(default=False)
    secret_key = models.CharField(max_length=255, blank=True, null=True)


class UserDeviceToken(BaseModel):
    """
    User Device Token Model

    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_device_token")
    device_name = models.CharField(max_length=100, blank=True, null=True)
    device_id = models.CharField(max_length=100, blank=True, null=True)
    fcm_token = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
