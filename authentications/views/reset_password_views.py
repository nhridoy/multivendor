import json

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import (
    generics,
    status,
    viewsets,
)  # noqa
from rest_framework.response import Response

from authentications import models, serializers
from utils import helper


# ============***********============
# Password reset views
# ============***********============
class PasswordResetView(generics.GenericAPIView):
    serializer_class = serializers.EmailSerializer
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        email = request.data.get("email")
        userModel = get_user_model()
        try:
            return self.__user_validate_and_send_token(userModel, email)
        except userModel.DoesNotExist:
            return Response(
                {"message": "User not found with this email"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def __user_validate_and_send_token(self, userModel, email):
        user = userModel.objects.get(email=email)

        # protocols
        http_host = self.request.META.get("HTTP_HOST")
        http_ref = self.request.META.get("HTTP_ORIGIN", "127.0.0.1:8000")
        # Encryption
        token = PasswordResetTokenGenerator().make_token(user)
        encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
        to_enc = {"token": token, "enc_pk": encoded_pk, "ref": http_ref}
        enc_token = helper.encode(str(to_enc))
        token_u = str(enc_token, "UTF-8")
        # Send the one-time password to the user's email or phone number
        protocol = "http://" if "http" not in http_host else ""
        url = f"{protocol}{http_host}/api/auth/password-verify/?token={token_u}"

        try:
            user_name = (
                    user.user_information.first_name + " " + user.user_information.last_name
            )
        except:
            user_name = "Dear"

        # templated_email_send(
        #     subject="Password Reset Request",
        #     send_to=[user.email],
        #     context={"reset_link": url, "user_name": user_name},
        #     template="reset_email.html",
        #     email_from="Reset Password <support@test.com>",
        # )
        return Response(
            {
                "message": "Reset Email sent",
                "token": enc_token,
                "url_token": token_u,
                "data": url,
            },
            status=status.HTTP_200_OK,
        )


class PasswordResetOTPVerifyView(generics.GenericAPIView):
    serializer_class = serializers.PasswordResetVerifySerializer
    permission_classes = []
    authentication_classes = []

    def post(self, request, token):
        serializer = serializers.PasswordResetVerifySerializer(
            data=request.data, context={"token": token}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {"message": "OTP Verified", "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(viewsets.ModelViewSet):
    serializer_class = serializers.PasswordResetSerializer
    permission_classes = []

    def post(self, request, token):
        serializer = serializers.PasswordResetSerializer(
            data=request.data, context={"token": token}
        )
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Password changed"})

    def verify_token(self, request, *args, **kwargs):
        token = self.request.query_params.get("token", None)

        # validate token
        user, key, ref = self._validate_user(token)
        if user or key:
            # redirect to frontend with token
            return redirect(to=f"{ref}/reset-password/{token}")
        return redirect(to=f"{ref}/")

    def _validate_user(self, token):
        """
        Verify token and encoded_pk and then set new password.
        """
        # decode token
        _decrypted_data = helper.decode(str(token))
        # replace all single quote with double quote
        _decrypted_data_dict = json.loads(_decrypted_data.replace("'", '"'))

        token = _decrypted_data_dict["token"]
        encoded_pk = _decrypted_data_dict["enc_pk"]
        ref = _decrypted_data_dict["ref"]

        if token is None or encoded_pk is None:
            return Response(
                {"detail": "Missing value"}, status=status.HTTP_400_BAD_REQUEST
            )

        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = models.User.objects.get(pk=pk)
        if not PasswordResetTokenGenerator().check_token(user, token):
            return None, None, ref
        return user, _decrypted_data_dict, ref
