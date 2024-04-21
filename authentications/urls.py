from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView
)
from rest_framework.routers import DefaultRouter
from authentications.views import CustomTokenObtainPairView, ChangePasswordView, NewUserView
from authentications.views.reset_password_views import PasswordResetView, PasswordResetConfirmView

router = DefaultRouter()
router.register(r'register', NewUserView, basename='register')

urlpatterns = [

    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('password-change/', ChangePasswordView.as_view(), name='change_password'),
    # reset password
    path("password-reset/", PasswordResetView.as_view(), name="request-password-reset", ),
    path("password-verify/", PasswordResetConfirmView.as_view({"get": "verify_token"}), name="password-verify", ),
    path("password-confirm/<str:token>/", PasswordResetConfirmView.as_view({"post": "post"}), name="reset-password", ),

]
urlpatterns += router.urls
