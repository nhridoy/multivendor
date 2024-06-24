import json

from dj_rest_auth.jwt_auth import unset_jwt_cookies
from django.conf import settings
from django.contrib.auth import get_user_model, logout, password_validation
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import generics, status, viewsets, views, exceptions
from rest_framework.response import Response

from authentications import models, serializers
from utils.extensions.permissions import IsAuthenticatedAndEmailVerified
from authentications.views.helper import generate_link, send_verification_email
from utils import helper
from utils.helper import decode_token, decrypt


# ============***********============
# Password reset views
# ============***********============
class ResetPasswordView(views.APIView):
    """
    View for getting email or sms for password reset
    post: username: ""
    """

    serializer_class = serializers.ResetPasswordSerializer
    authentication_classes = []
    permission_classes = []

    # throttle_classes = (AnonUserRateThrottle,)

    @staticmethod
    def email_sender_helper(user, origin):
        url = generate_link(user, origin, "reset-password")
        send_verification_email(user, url)

        return Response({"detail": "Email Sent", "is_email": True})

    def post(self, *args, **kwargs):
        try:
            origin = self.request.headers["origin"]
        except Exception as e:
            raise exceptions.PermissionDenied(
                detail="Origin not found on request header"
            ) from e
        ser = self.serializer_class(data=self.request.data)
        ser.is_valid(raise_exception=True)
        user = ser.user

        if user.email:
            return self.email_sender_helper(user, origin)

        raise exceptions.PermissionDenied(
            detail="No Email found!!!",
        )


class ResetPasswordCheckView(views.APIView):
    """
    View for checking if the url is expired or not
    post: token: ""
    """

    authentication_classes = []
    permission_classes = []
    serializer_class = serializers.ResetPasswordCheckSerializer

    def post(self, *args, **kwargs):
        ser = self.serializer_class(data=self.request.data)
        ser.is_valid(raise_exception=True)

        try:
            decode_token(token=decrypt(str(ser.data.get("token"))))

        except Exception as e:
            raise exceptions.APIException(detail=e) from e
        return Response({"data": "Accepted"})


class ResetPasswordConfirmView(views.APIView):
    """
    View for resetting password after checking the token
    post: token: "", password: ""
    """

    serializer_class = serializers.ResetPasswordConfirmSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, *args, **kwargs):
        ser = self.serializer_class(data=self.request.data)
        ser.is_valid(raise_exception=True)

        try:
            return self._change_password(ser)
        except Exception as e:
            raise exceptions.APIException(detail=e) from e

    @staticmethod
    def _change_password(ser):
        decoded = decode_token(token=decrypt(str(ser.data.get("token"))))

        if ser.validated_data.get("password") != ser.validated_data.get(
            "retype_password"
        ):
            raise exceptions.NotAcceptable(detail="Passwords doesn't match!!!")

        user = models.User.objects.get(id=decoded.get("user"))
        password_validation.validate_password(
            password=ser.data.get("password"), user=user
        )
        user.set_password(ser.data.get("password"))
        user.save()
        return Response({"detail": "Password Changed Successfully"})



class PasswordResetView(generics.GenericAPIView):
    serializer_class = serializers.ResetPasswordSerializer
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
