from rest_framework import (
    response,
    status,
    viewsets,
)  # noqa
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
    http_method_names = ["get", "post"]

    def create(self, request, *args, **kwargs):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        if new_user := serializer.save():
            host = request.META
            user_data = serializer.data
            tokens = RefreshToken.for_user(new_user)
            refresh = str(tokens)
            access = str(tokens.access_token)
            auth_data = {
                "user_data": user_data,
                "refresh": refresh,
                "access": access,
                "is_active": new_user.is_active,
            }

            return response.Response(data=auth_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
