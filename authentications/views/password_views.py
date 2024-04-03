from django.conf import settings
from django.contrib.auth import logout, password_validation
from django.shortcuts import redirect
from rest_framework import (
    exceptions,
    generics,
    permissions,
    response,
    status,
)
from authentications import serializers


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ChangePasswordSerializer

    @staticmethod
    def _logout_on_password_change(request):
        resp = response.Response(
            {"detail": "Password updated successfully"},
            status=status.HTTP_200_OK,
        )
        if settings.REST_SESSION_LOGIN:
            logout(request)
        redirect("/")
        return resp

    def _change_password(self, request, user, password):
        try:
            password_validation.validate_password(password=password, user=user)
            user.set_password(password)
            user.save()
            print(settings.LOGOUT_ON_PASSWORD_CHANGE)
            if settings.LOGOUT_ON_PASSWORD_CHANGE:
                self._logout_on_password_change(request=request)
            return True
        except Exception as e:
            return False

    def update(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check old password
        old_password = serializer.validated_data.get("old_password")
        if not user.check_password(old_password):
            return response.Response(
                {"detail": "You have entered Wrong password."},
                status=status.HTTP_403_FORBIDDEN,
            )
        # set_password also hashes the password that the user will get
        password = serializer.validated_data.get("password")
        retype_password = serializer.validated_data.get("retype_password")

        if password != retype_password:
            raise exceptions.NotAcceptable(detail="Passwords do not match")
        if self._change_password(
                request=request,
                user=user,
                password=password,
        ):
            return response.Response(
                {"detail": "Password updated successfully"},
                status=status.HTTP_200_OK,
            )
        return response.Response(
            {"detail": "Password updated Failed"},
            status=status.HTTP_403_FORBIDDEN,
        )

# reset password
