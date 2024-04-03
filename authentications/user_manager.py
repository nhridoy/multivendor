from django.contrib.auth.models import BaseUserManager

from django.db import transaction


class UserManager(BaseUserManager):
    """
    This is the manager for custom user model
    """

    @transaction.atomic
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError("Username should not be empty")

        if not password:
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
    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user
