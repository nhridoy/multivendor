from django.urls import path
from rest_framework.routers import DefaultRouter

from notifications.views import NotificationsView, FcmAPIView

router = DefaultRouter()

router.register('notifications', NotificationsView, basename='notifications')

urlpatterns = [
    path('push-notifications/', FcmAPIView.as_view({"post": "post"}), name='push_notifications'),
]
urlpatterns += router.urls
