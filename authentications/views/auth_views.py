from django.conf import settings
from django.contrib.auth import login
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from authentications.auth_backend import EmailPhoneUsernameAuthenticationBackend as EPUA
from authentications.serializers import CustomTokenObtainPairSerializer
from utils.modules import EmailSender
from utils.modules.otp_verifications import OTPVerification


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
            if not user.user_two_step_verification.is_active:
                data = self.__direct_login(request, user, serializer)
                return Response({'data': data, "detail": "Login Successful"}, status=status.HTTP_200_OK)
            else:
                # generate otp code
                otp = OTPVerification(secret_key=user.user_two_step_verification.secret_key, digit=6)
                if 'otp' in request.data:
                    # if otp code is provided
                    return self.verify_otp(request, user, serializer, otp)
                # otp_code = otp.generate_otp()

                # email send for otp code
                self.send_otp_email(user, otp)

                return Response({"detail": "One Time Password sent"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED
            )

    def verify_otp(self, request, user, ser, otp_obj):
        otp = request.data.get("otp")

        if otp_obj.verify_otp(otp):
            data = self.__direct_login(request, user, ser)
            return Response({'data': data, "detail": "Login Successful"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def __direct_login(request, user, ser):
        login(request, user)
        data = ser.validated_data
        return data

    @staticmethod
    def send_otp_email(user, obj):
        context = {
            "name": "test",
            "company": "potentail",
            "procedure": "Login",
            "valid_time": "5 minutes",

        }
        obj.send_otp([user.email], context)
        return
