from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from authentications.views import (
    AppleLoginView,
    ChangePasswordView,
    CustomTokenObtainPairView,
    GoogleLoginView,
    KakaoLoginView,
    NewUserView,
    PasswordValidateView,
)
from authentications.views.reset_password_views import (
    PasswordResetConfirmView,
    PasswordResetView,
    ResetPasswordView,
)

router = DefaultRouter()
router.register(r"register", NewUserView, basename="register")
password_urls = [
    path("password-validate/", PasswordValidateView.as_view()),
    path("password-change/", ChangePasswordView.as_view(), name="change_password"),
    path("password-reset/", ResetPasswordView.as_view()),
    # path("password-reset-check/", ResetPasswordCheckView.as_view()),
    # path("password-reset-confirm/", ResetPasswordConfirmView.as_view()),
    path("password-change/", ChangePasswordView.as_view(), name="change_password"),
    # reset password
    path(
        "password-reset/",
        ResetPasswordView.as_view(),
        name="request-password-reset",
    ),
    path(
        "password-verify/",
        PasswordResetConfirmView.as_view({"get": "verify_token"}),
        name="password-verify",
    ),
    path(
        "password-confirm/<str:token>/",
        PasswordResetConfirmView.as_view({"post": "post"}),
        name="reset-password",
    ),
]
login_urls = [
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
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
urlpatterns += signup_urls
urlpatterns += password_urls
urlpatterns += social_urls
