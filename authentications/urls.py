from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenVerifyView

from authentications.views import (
    AdminUserViewSet,
    AppleLoginView,
    ChangePasswordView,
    GoogleLoginView,
    KakaoLoginView,
    LoginView,
    LogoutView,
    MyTokenRefreshView,
    OTPCheckView,
    OTPLoginView,
    OTPView,
    PasswordValidateView,
    RegistrationView,
)
from authentications.views.reset_password_views import (
    ResetPasswordCheckView,
    ResetPasswordConfirmView,
    ResetPasswordView,
)

router = DefaultRouter()
router.register(r"register", RegistrationView, basename="register")
router.register(r"admin/user", AdminUserViewSet, basename="admin-user")

password_urls = [
    path("password-validate/", PasswordValidateView.as_view()),
    path("password-change/", ChangePasswordView.as_view(), name="change_password"),
    # reset password
    path(
        "password-reset/",
        ResetPasswordView.as_view(),
        name="request-password-reset",
    ),
    path(
        "password-reset-check/",
        ResetPasswordCheckView.as_view(),
        name="password-verify",
    ),
    path("password-reset-confirm/", ResetPasswordConfirmView.as_view()),
]
login_urls = [
    path("login/user/", LoginView.as_view(), name="user-login"),
    path("login/admin/", LoginView.as_view(), name="admin-login"),
    path("otp-login/", OTPLoginView.as_view(), name="otp-login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", MyTokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
otp_urls = [
    path("otp-check/", OTPCheckView.as_view(), name="otp-check"),
    path("otp/", OTPView.as_view(), name="otp"),
]
signup_urls = []
social_urls = [
    path("google/", GoogleLoginView.as_view()),
    path("kakao/", KakaoLoginView.as_view()),
    path("apple/", AppleLoginView.as_view()),
]
urlpatterns = []
urlpatterns += router.urls
urlpatterns += login_urls
urlpatterns += otp_urls
urlpatterns += signup_urls
urlpatterns += password_urls
urlpatterns += social_urls
