from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView
)

from authentications.views import CustomTokenObtainPairView, ChangePasswordView

urlpatterns = [

    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('password-change/', ChangePasswordView.as_view(), name='change_password'),
]
