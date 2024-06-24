from django.contrib.auth.models import BaseUserManager
from django.db import transaction


class UserManager(BaseUserManager):
    """
    This is the manager for custom user model
    """

    @transaction.atomic
    def create_user(self, username, email, password=None, oauth_provider=None):
        if not username:
            raise ValueError("Username should not be empty")

        if not oauth_provider:
            raise ValueError("oauth_provider should not be empty")

        if oauth_provider == "email" and not password:
            raise ValueError("Password should not be empty")

        if email:
            user = self.model(
                username=username,
                email=self.normalize_email(email=email),
            )
        else:
            user = self.model(
                username=username,
            )
        user.set_password(password)
        user.save(using=self._db)
        return user

    @transaction.atomic
    def create_superuser(self, username, email, password=None, oauth_provider="email"):
        if not password:
            raise ValueError("Password should not be empty")

        user = self.create_user(
            username=username, email=email, password=password, oauth_provider=oauth_provider
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user
