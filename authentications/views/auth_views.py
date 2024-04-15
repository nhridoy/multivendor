from django.contrib.auth import login
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from authentications.auth_backend import EmailPhoneUsernameAuthenticationBackend as EPUA
from authentications.serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = EPUA.authenticate(
                request=request,
                username=(request.data.get("username")).strip(),
                password=request.data.get("password"),
            )
            data = self.__direct_login(request, user, serializer)
            return Response({'data': data, "detail": "Login Successful"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED
            )

    @staticmethod
    def __direct_login(request, user, ser):
        login(request, user)
        data = ser.validated_data
        return data
