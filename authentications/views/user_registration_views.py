from django.conf import settings
from rest_framework import (
    response,
    status,
    viewsets,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from authentications import serializers
from authentications.models import User


class NewUserView(viewsets.ModelViewSet):
    """
    New User Create View
    """

    serializer_class = serializers.NewUserSerializer
    queryset = User.objects.all()
    permission_classes = []
    authentication_classes = []
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        if new_user := serializer.save():
            user_data = serializer.data
            tokens = RefreshToken.for_user(new_user)
            refresh = str(tokens)
            access = str(tokens.access_token)
            auth_data = {
                "refresh": refresh,
                "access": access,
                "user": user_data,
            }
            if settings.OTP_ENABLED:
                # send otp
                pass
            return response.Response(data=auth_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def __sent_otp(self, user):
        pass