from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView
)
from rest_framework.routers import DefaultRouter
from authentications.views import CustomTokenObtainPairView, ChangePasswordView, NewUserView

router = DefaultRouter()
router.register(r'register', NewUserView, basename='register')

urlpatterns = [

    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('password-change/', ChangePasswordView.as_view(), name='change_password'),

]
urlpatterns += router.urls
