from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from authentications import models


# Register your models here.
class AdminUser(UserAdmin):
    ordering = ("-date_joined",)
    search_fields = (
        "username",
        "email",
    )
    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "is_verified",
    )
    list_display = (
        "username",
        "email",
        "oauth_provider",
        "date_joined",
        "is_verified",
        "is_active",
    )
    fieldsets = (
        (
            "Login Info",
            {
                "fields": (
                    "username",
                    "email",
                    "password",
                    "oauth_provider",
                    "is_verified",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "oauth_provider",
                    "is_verified",
                ),
            },
        ),
    )


class AdminUserInformation(admin.ModelAdmin):
    ordering = ("-created_at",)
    autocomplete_fields = (
        "user",
        "country",
        "province",
        "city",
    )
    search_fields = (
        "user__username",
        "user__email",
        "full_name",
        "phone_number",
    )
    list_filter = ("gender",)
    list_display = (
        "user",
        "full_name",
        "gender",
        "country",
        "province",
        "city",
        "created_at",
    )
    fieldsets = (
        ("User", {"fields": ("user",)}),
        (
            "User Information",
            {
                "fields": (
                    "full_name",
                    "gender",
                    "profile_picture",
                    "date_of_birth",
                )
            },
        ),
        (
            "Contact Information",
            {
                "fields": (
                    "language",
                    "address",
                    "country",
                    "province",
                    "city",
                    "phone_number",
                    "is_phone_verified",
                )
            },
        ),
    )


class AdminOTPModel(admin.ModelAdmin):
    autocomplete_fields = ("user",)
    exclude = ("is_active",)
    search_fields = (
        "user__username",
        "user__email",
    )


admin.site.register(models.User, AdminUser)
admin.site.register(models.UserInformation, AdminUserInformation)
admin.site.register(models.UserTwoStepVerification, AdminOTPModel)
